import base64

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from djoser.serializers import UserSerializer
from rest_framework import serializers

from recipes.constants import RecipesModels
from recipes.models import (
    Favorite,
    Ingredient,
    Recipe,
    RecipeIngredient,
    RecipeTag,
    ShoppingCart,
    Tag,
    Unit,
)
from users.models import Subscription

User = get_user_model()


class CustomUserSerializer(UserSerializer):
    """Сериализатор пользователя."""
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )
        read_only_fields = fields

    def get_is_subscribed(self, author):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.subscriptions.filter(author=author).exists()


class SubscriptionsSerializer(CustomUserSerializer):
    """Сериализатор подписок."""
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta(CustomUserSerializer.Meta):
        fields = (
            *CustomUserSerializer.Meta.fields,
            'recipes',
            'recipes_count',
        )
        read_only_fields = ('username', 'email', 'first_name', 'last_name')

    def validate(self, data):
        request = self.context.get('request')
        user = request.user
        if request.method == 'POST':
            author = self.context.get('author')
            if author == user:
                raise serializers.ValidationError(
                    detail="Нельзя подписаться на самого себя."
                )
            if Subscription.objects.filter(author=author, user=user).exists():
                raise serializers.ValidationError(
                    detail="Вы уже подписаны на этого пользователя."
                )
        if request.method == 'DELETE':
            author = self.instance
            if not Subscription.objects.filter(
                author=author, user=user
            ).exists():
                raise serializers.ValidationError(
                    detail="Вы не подписаны на этого пользователя."
                )
        return data

    def create(self, validated_data):
        return Subscription.objects.create(**validated_data).author

    def get_recipes(self, author):
        print(author)
        request = self.context.get('request')
        recipes_limit = request.GET.get('recipes_limit')
        recipes = author.recipes.all()
        if recipes_limit:
            recipes = recipes[: int(recipes_limit)]
        serializer = RecipesShortSerializer(recipes, many=True)
        return serializer.data

    def get_recipes_count(self, author):
        return author.recipes.count()


class TagsSerializer(serializers.ModelSerializer):
    """Сериализатор тегов."""
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class UnitsSerializer(serializers.ModelSerializer):
    """Сериализатор единиц измерения."""
    class Meta:
        model = Unit
        fields = ('id', 'name')


class IngredientsSerializer(serializers.ModelSerializer):
    """Сериализатор иингридиентов."""
    measurement_unit = serializers.SlugRelatedField(
        read_only=True, slug_field="name"
    )

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class Base64ImageField(serializers.ImageField):
    """Класс для преобразования картинки."""
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]

            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class RecipesIngredientsReadSerializer(serializers.ModelSerializer):
    """Сериализатор иингридиентов рецепта."""
    id = serializers.PrimaryKeyRelatedField(
        source='ingredient.id', read_only=True
    )
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit.name'
    )

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipesIngredientsWriteSerializer(serializers.ModelSerializer):
    """Сериализатор записи иингридиентов."""
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'amount')


class RecipesReadSerializer(serializers.ModelSerializer):
    """Сериализатор чтения рецептов."""
    tags = TagsSerializer(many=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = RecipesIngredientsReadSerializer(
        source='recipe_ingredients', many=True
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'image',
            'text',
            'cooking_time',
        )

    def get_is_favorited(self, recipe):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.favorite.filter(recipe=recipe).exists()

    def get_is_in_shopping_cart(self, recipe):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.shoppingcart.filter(recipe=recipe).exists()


class RecipesWriteSerializer(serializers.ModelSerializer):
    """Сериализатор записи рецептов."""
    author = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )
    ingredients = RecipesIngredientsWriteSerializer(required=True, many=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True
    )
    image = Base64ImageField()
    cooking_time = serializers.IntegerField(
        min_value=RecipesModels.MIN_POS_INT.value,
        max_value=RecipesModels.MAX_COOKING_TIME.value,
    )

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'author',
            'ingredients',
            'tags',
            'image',
            'text',
            'cooking_time',
        )

    def validate(self, data):
        if not data.get('ingredients'):
            raise serializers.ValidationError(
                {'ingredients': 'Обязательное поле.'}
            )
        if not data.get('tags'):
            raise serializers.ValidationError({'tags': 'Обязательное поле.'})
        return data

    def validate_ingredients(self, value):
        if not value:
            raise serializers.ValidationError(
                {'ingredients': 'Это поле не может быть пустым.'}
            )
        ingredients_list = []
        for item in value:
            ingredient = item.get('id')
            if ingredient in ingredients_list:
                raise serializers.ValidationError(
                    {'ingredients': 'Ингридиенты не должны повторяться.'}
                )
            ingredients_list.append(ingredient)
        return value

    def validate_tags(self, value):
        if not value:
            raise serializers.ValidationError(
                {'tags': 'Это поле не может быть пустым.'}
            )
        tags_set = set(value)
        if len(value) != len(tags_set):
            raise serializers.ValidationError(
                {'tags': 'Теги не должны повторяться.'}
            )
        return value

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        instance = super().create(validated_data)
        RecipeIngredient.objects.bulk_create(
            [
                RecipeIngredient(
                    recipe=instance,
                    ingredient=ingredient.get('id'),
                    amount=ingredient.get('amount'),
                )
                for ingredient in ingredients
            ]
        )
        RecipeTag.objects.bulk_create(
            [
                RecipeTag(recipe=instance, tag=tag_instance)
                for tag_instance in tags
            ]
        )
        instance.save()
        return instance

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        instance.ingredients.clear()
        instance.tags.clear()
        RecipeIngredient.objects.bulk_create(
            [
                RecipeIngredient(
                    recipe=instance,
                    ingredient=ingredient.get('id'),
                    amount=ingredient.get('amount'),
                )
                for ingredient in ingredients
            ]
        )
        RecipeTag.objects.bulk_create(
            [
                RecipeTag(recipe=instance, tag=tag_instance)
                for tag_instance in tags
            ]
        )
        instance = super().update(instance, validated_data)
        instance.save()
        return instance

    def to_representation(self, instance):
        serializer = RecipesReadSerializer(
            instance, context={'request': self.context.get('request')}
        )
        return serializer.data


class RecipesShortSerializer(serializers.ModelSerializer):
    """Сериализатор кратких рецептов."""
    image = Base64ImageField(read_only=True)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )
        read_only_fields = (
            'id',
            'name',
            'cooking_time',
        )


class FavoritesSerializer(RecipesShortSerializer):
    """Сериализатор избранного."""
    class Meta(RecipesShortSerializer.Meta):
        fields = [*RecipesShortSerializer.Meta.fields]

    def validate(self, data):
        request = self.context.get('request')
        user = request.user
        if request.method == 'POST':
            recipe = self.context.get('recipe')
            if Favorite.objects.filter(user=user, recipe=recipe).exists():
                raise serializers.ValidationError(
                    detail='Рецепт уже в избранном.'
                )
        if request.method == 'DELETE':
            recipe = self.instance
            if not Favorite.objects.filter(user=user, recipe=recipe).exists():
                raise serializers.ValidationError(
                    detail='Рецепта нет в избранном.'
                )
        return data

    def create(self, validated_data):
        return Favorite.objects.create(**validated_data).recipe


class ShoppingCartSerializer(RecipesShortSerializer):
    """Сериализатор корзины покупок."""
    class Meta(RecipesShortSerializer.Meta):
        fields = [*RecipesShortSerializer.Meta.fields]

    def validate(self, data):
        request = self.context.get('request')
        user = request.user
        if request.method == 'POST':
            recipe = self.context.get('recipe')
            if ShoppingCart.objects.filter(user=user, recipe=recipe).exists():
                raise serializers.ValidationError(
                    detail='Рецепт уже в списке покупок.'
                )
        if request.method == 'DELETE':
            recipe = self.instance
            if not ShoppingCart.objects.filter(
                user=user, recipe=recipe
            ).exists():
                raise serializers.ValidationError(
                    detail='Рецепта нет в списке покупок.'
                )
        return data

    def create(self, validated_data):
        return ShoppingCart.objects.create(**validated_data).recipe
