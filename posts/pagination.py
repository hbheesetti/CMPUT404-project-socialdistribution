from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


DEFAULT_PAGE = 1
DEFAULT_PAGE_SIZE = 5


class CustomCommentPagination(PageNumberPagination):
    page_size = DEFAULT_PAGE_SIZE
    page_size_query_param = 'size'
    max_page_size = 10
    page_query_param = 'page'
    def get_paginated_response(self, data, post, id):
        return Response({
            'type': 'comments',
            'page': int(self.request.GET.get('page', DEFAULT_PAGE)),
            'size': int(self.request.GET.get('size', 5)),
            'post': post,
            'id': id,
            'comments': data
        })