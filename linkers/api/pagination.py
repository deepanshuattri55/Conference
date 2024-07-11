from rest_framework.pagination import CursorPagination

class EditorConferenceCursorPagination(CursorPagination):
    page_size = 10
    ordering = '-conference__end_date'
    cursor_query_param = 'editor'

class ReviewerConferenceCursorPagination(CursorPagination):
    page_size = 10
    ordering = '-conference__end_date'
    cursor_query_param = 'reviewer'

class ReviewerPaperCursorPagination(CursorPagination):
    page_size = 10
    ordering = '-paper__conference__end_date'
    cursor_query_param = 'paper'