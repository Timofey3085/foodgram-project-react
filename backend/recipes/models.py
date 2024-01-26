from colorfield.fields import ColorField
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from recipes.constants import RecipesModels

User = get_user_model()


class Tag(models.Model):
    """Модель тега."""
    name = models.CharField(
        max_length=RecipesModels.MAX_LEN_TAG_NAME.value,
        unique=True,
        verbose_name='Название',
    )
    color = ColorField(format='hex', verbose_name='Цвет в формате HEX',
                       unique=True,)
    slug = models.SlugField(unique=True, verbose_name='Слаг')

    class Meta:
        ordering = ['name']
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Unit(models.Model):
    """Модель единицы измерения."""
    name = models.CharField(
        max_length=RecipesModels.MAX_LEN_UNIT_NAME.value,
        unique=True,
        verbose_name='Название',
    )

    class Meta:
        verbose_name = 'Единица измерения'
        verbose_name_plural = 'Единицы измерения'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Модель ингридиента."""
    name = models.CharField(
        max_length=RecipesModels.MAX_LEN_INGREDIENT_NAME.value,
        verbose_name='Название',
    )
    measurement_unit = models.ForeignKey(
        Unit,
        related_name='ingredients',
        on_delete=models.CASCADE,
        verbose_name='Единица измерения',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'], name='unique_ingredient'
            )
        ]
        ordering = ['name']
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Модель рецета."""
    tags = models.ManyToManyField(
        Tag, through='RecipeTag', verbose_name='Теги'
    )
    author = models.ForeignKey(
        User,
        related_name='recipes',
        on_delete=models.CASCADE,
        verbose_name='Автор',
    )
    ingredients = models.ManyToManyField(
        Ingredient, through='RecipeIngredient', verbose_name='Ингредиенты'
    )
    name = models.CharField(
        max_length=RecipesModels.MAX_LEN_RECIPE_NAME.value,
        verbose_name='Название',
    )
    image = models.ImageField(
        upload_to='recipes/images/', verbose_name='Изображение'
    )
    text = models.TextField(verbose_name='Описание')
    cooking_time = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(
                RecipesModels.MIN_POS_INT.value,
                (
                    'Время приготовления не может быть меньше '
                    f'{RecipesModels.MIN_POS_INT.value} минуты.'
                ),
            ),
            MaxValueValidator(
                RecipesModels.MAX_COOKING_TIME.value,
                (
                    'Время приготовления не может быть больше '
                    f'{RecipesModels.MAX_COOKING_TIME.value} минут.'
                ),
            ),
        ],
        verbose_name='Время приготовления, мин.',
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class RecipeTag(models.Model):
    """Модель тега рецепта."""
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, verbose_name='Рецепт'
    )
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, verbose_name='Тег')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'tag'], name='unique_recipe_tag'
            )
        ]
        verbose_name = 'Тег рецепта'
        verbose_name_plural = 'Теги рецепта'

    def __str__(self):
        return f'{self.recipe} - {self.tag}'


class RecipeIngredient(models.Model):
    """Модель связи моделей рецептов и ингредиентов."""
    recipe = models.ForeignKey(
        Recipe,
        related_name='recipe_ingredients',
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
    )
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, verbose_name='Ингредиент'
    )
    amount = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(
                RecipesModels.MIN_POS_INT.value,
                (
                    'Количество не может быть меньше '
                    f'{RecipesModels.MIN_POS_INT.value}.'
                ),
            )
        ],
        verbose_name='Количество',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_recipe_ingredient',
            )
        ]
        ordering = ['recipe']
        verbose_name = 'Ингредиент рецепта'
        verbose_name_plural = 'Ингредиенты рецепта'

    def __str__(self):
        return f'{self.recipe} - {self.amount} {self.ingredient}'


class UserRecipe(models.Model):
    """Модель пользовательского рецепта."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
    )

    class Meta:
        abstract = True
        default_related_name = '%(model_name)s'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'], name='unique_%(class)s'
            )
        ]

    def __str__(self):
        return f'{self.user} - {self.recipe}'


class Favorite(UserRecipe):
    """Модель избранного."""
    class Meta(UserRecipe.Meta):
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        ordering = ['user']

    def __str__(self):
        return self.user


class ShoppingCart(UserRecipe):
    """Модель списка покупок."""
    class Meta(UserRecipe.Meta):
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзина'
        ordering = ['user']

    def __str__(self):
        return self.user
