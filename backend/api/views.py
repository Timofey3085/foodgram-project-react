from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response

from recipes.models import (
    Favorite,
    Ingredient,
    Recipe,
    RecipeIngredient,
    ShoppingCart,
    Tag,
)
from users.models import Subscription

from .filters import IngredientFilter, RecipesFilter
from .paginations import CustomPageNumberPagination
from .permissions import IsAuthenticatedAuthorOrReadOnly
from .serializers import (
    CustomUserSerializer,
    FavoritesSerializer,
    IngredientsSerializer,
    RecipesReadSerializer,
    RecipesWriteSerializer,
    ShoppingCartSerializer,
    SubscriptionsSerializer,
    TagsSerializer,
)

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    """ViewSet для работы с пользователями."""
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = CustomPageNumberPagination

    @action(['post'], detail=True, permission_classes=[IsAuthenticated])
    def subscribe(self, request, id=None):
        author = self.get_object()
        serializer = SubscriptionsSerializer(
            data=request.data,
            context={'request': request, 'author': author},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(author=author, user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @subscribe.mapping.delete
    def delete_subscribe(self, request, id=None):
        author = self.get_object()
        serializer = SubscriptionsSerializer(
            author, data=request.data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        get_object_or_404(
            Subscription, author=author, user=request.user
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(['get'], detail=False, permission_classes=[IsAuthenticated])
    def subscriptions(self, request):
        queryset = User.objects.filter(subscribers__user=request.user)
        pages = self.paginate_queryset(queryset)
        serializer = SubscriptionsSerializer(
            pages, many=True, context={'request': request}
        )
        return self.get_paginated_response(serializer.data)


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    """VieSet для тегов."""
    queryset = Tag.objects.all()
    serializer_class = TagsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для ингредиентов."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = IngredientFilter


class RecipesViewSet(viewsets.ModelViewSet):
    """ViewSet для рецептов."""
    queryset = Recipe.objects.all()
    permission_classes = [IsAuthenticatedAuthorOrReadOnly]
    pagination_class = CustomPageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipesFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipesReadSerializer
        return RecipesWriteSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(["post"], detail=True, permission_classes=[IsAuthenticated])
    def favorite(self, request, pk=None):
        recipe = self.get_object()
        serializer = FavoritesSerializer(
            data=request.data,
            context={'request': request, 'recipe': recipe},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, recipe=recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @favorite.mapping.delete
    def delete_favorite(self, request, pk=None):
        recipe = self.get_object()
        serializer = FavoritesSerializer(
            recipe, data=request.data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        get_object_or_404(Favorite, user=request.user, recipe=recipe).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(['post'], detail=True, permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk=None):
        recipe = self.get_object()
        serializer = ShoppingCartSerializer(
            data=request.data,
            context={'request': request, 'recipe': recipe},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, recipe=recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk=None):
        recipe = self.get_object()
        serializer = ShoppingCartSerializer(
            recipe, data=request.data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        get_object_or_404(
            ShoppingCart, user=request.user, recipe=recipe
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['get'], detail=False, url_path='download_shopping_cart',
            permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        user = request.user
        ingredients = (
            RecipeIngredient.objects.filter(
                recipe__shoppingcart__user=request.user
            )
            .order_by('ingredient__name')
            .values('ingredient__name', 'ingredient__measurement_unit__name')
            .annotate(amount=Sum('amount'))
        )
        shopping_list = 'Список покупок\n\n'
        shopping_list += '\n'.join(
            [
                (
                    f'- {ingredient["ingredient__name"]} '
                    f'({ingredient["ingredient__measurement_unit__name"]})'
                    f' - {ingredient["amount"]}'
                )
                for ingredient in ingredients
            ]
        )
        response = FileResponse(shopping_list, content_type='txt')
        response[
            'Content-Disposition'
        ] = f'attachment; filename={user.username}_shopping_list.txt'
        return response
