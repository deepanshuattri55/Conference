from rest_framework.pagination import CursorPagination

class PaperCursorPagination(CursorPagination):
    page_size = 10;
    ordering = 'last_modified'
    cursor_query_param = 'record'