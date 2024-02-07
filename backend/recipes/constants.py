from enum import Enum


class Pagination(Enum):
    PAGE_SIZE = 6


class RecipesModels(Enum):
    MAX_LEN_TAG_NAME = 200
    MAX_LEN_UNIT_NAME = 200
    MAX_LEN_INGREDIENT_NAME = 200
    MAX_LEN_RECIPE_NAME = 200
    MAX_COOKING_TIME = 1440
    MIN_POS_INT = 1


class UsersModels(Enum):
    MAX_LEN_USER_FIRST_NAME = 150
    MAX_LEN_USER_LAST_NAME = 150
