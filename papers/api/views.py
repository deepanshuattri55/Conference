from django.shortcuts import get_object_or_404
from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render
from .serializers import PaperSerializer
from papers.models import Paper
from conferences.models import Conference
from . import pagination

class PaperListView(generics.ListAPIView):
    serializer_class = PaperSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = pagination.PaperCursorPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'keyword', 'conference__title']
    ordering_fields = ['title', 'last_modified']

    def get_queryset(self):
        user = self.request.user
        return Paper.objects.filter(user=user).select_related('conference', 'user')
    
    def get_view_name(self):
        return "List of Papers (User)"

class PaperDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PaperSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Paper.objects.filter(user=user).select_related('conference', 'user')
    
    def get_view_name(self):
        return "Detail View of Paper (User)"

class PaperCreateView(generics.CreateAPIView):
    serializer_class = PaperSerializer
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        return render(request, 'html/Authors_new_submission.html')

    def perform_create(self, serializer):
        conf_acronym = self.kwargs.get('conf')
        conference = get_object_or_404(Conference, acronym=conf_acronym)
        serializer.save(user=self.request.user, conference=conference)
# class PaperCreateView(generics.CreateAPIView):
#     serializer_class = PaperSerializer
#     permission_classes = [IsAuthenticated]

#     def perform_create(self, serializer):
#         conf_acronym = self.kwargs.get('conf')
#         conference = get_object_or_404(Conference, acronym=conf_acronym)
#         serializer.save(user=self.request.user, conference=conference)
#         # Render the template after successful creation
#         return render(self.request, 'authors_new_submission.html', {
#             'conference': conference,
#             'user': self.request.user
#         })    
    def get_view_name(self):
        return "Submit Paper to Conference"