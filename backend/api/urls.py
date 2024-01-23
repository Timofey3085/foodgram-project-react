from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CustomUserViewSet, IngredientsViewSet, RecipesViewSet,
                    TagsViewSet)

app_name = "api"

v1_router = DefaultRouter()

v1_router.register('users', CustomUserViewSet, basename='users')
v1_router.register('tags', TagsViewSet, basename='tags')
v1_router.register('ingredients', IngredientsViewSet, basename='ingredients')
v1_router.register('recipes', RecipesViewSet, basename='recipes')

urlpatterns = [
    path("", include(v1_router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]
