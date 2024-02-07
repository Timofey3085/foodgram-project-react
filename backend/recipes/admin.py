import csv

from django import forms
from django.contrib import admin
from django.shortcuts import redirect, render
from django.urls import path

from .models import (Favorite, Ingredient, Recipe, RecipeIngredient, RecipeTag,
                     ShoppingCart, Tag, Unit)


class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'color', 'slug']
    search_fields = ['name', 'color', 'slug']


class UnitAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


class CsvImportForm(forms.Form):
    csv_file = forms.FileField()


def decode_utf8(input_iterator):
    for i in input_iterator:
        yield i.decode('utf-8')


class IngredientAdmin(admin.ModelAdmin):
    change_list_template = "recipes/change_list.html"
    list_display = ['id', 'name', 'measurement_unit']
    search_fields = ['name']
    list_filter = ['measurement_unit']

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('import-csv/', self.import_csv),
        ]
        return my_urls + urls

    def import_csv(self, request):
        if request.method == 'POST':
            csv_file = request.FILES['csv_file']
            reader = csv.reader(decode_utf8(csv_file), delimiter=';')
            for i, row in enumerate(reader):
                if i == 0:
                    continue
                name = row[0]
                measurement_unit_name = row[1]
                unit, _ = Unit.objects.get_or_create(
                    name=measurement_unit_name)
                Ingredient.objects.get_or_create(
                    name=name, measurement_unit=unit)
            self.message_user(request, 'Ваш csv фаил импортирован')
            return redirect('..')
        form = CsvImportForm()
        payload = {'form': form}
        return render(
            request, "recipes/import_form.html", payload
        )


class RecipeAdmin(admin.ModelAdmin):
    list_display = [
        'author',
        'id',
        'name',
        'cooking_time',
        'favorite_added',
    ]
    search_fields = ['author', 'name', 'text']
    list_filter = ['tags__name', 'ingredients__name']
    readonly_fields = ['favorite_added']

    def favorite_added(self, obj):
        return obj.favorite.all().count()

    favorite_added.short_description = "Количество добавлений в избранное"


class RecipeTagAdmin(admin.ModelAdmin):
    list_display = ['recipe', 'tag']
    search_fields = ['recipe', 'tag']


class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ['recipe', 'ingredient', 'amount']
    search_fields = ['recipe', 'ingredient']


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['recipe', 'user']
    search_fields = ['recipe', 'user']
    list_filter = ['recipe', 'user']


class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ['user']
    search_fields = ['user']


admin.site.register(Tag, TagAdmin)
admin.site.register(Unit, UnitAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeTag, RecipeTagAdmin)
admin.site.register(RecipeIngredient, RecipeIngredientAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
