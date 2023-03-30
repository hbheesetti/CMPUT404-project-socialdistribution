from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

DEFAULT_PAGE = 1
DEFAULT_PAGE_SIZE = 50

class CustomPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'size'
    max_page_size = 100
    def get_paginated_response(self, data, type):
        return Response({
            'type': type,
            'page': int(self.request.GET.get('page', DEFAULT_PAGE)),
            'size': int(self.request.GET.get('size', DEFAULT_PAGE_SIZE)),
            'items': data
        })