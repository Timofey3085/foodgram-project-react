from recipes.constants import Pagination
from rest_framework.pagination import PageNumberPagination


class CustomPageNumberPagination(PageNumberPagination):
    """Кастомный класс пагинатора."""
    page_size_query_param = "limit"
    page_size = Pagination.PAGE_SIZE.value
