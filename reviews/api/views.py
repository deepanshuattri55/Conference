from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.response import Response

from papers.models import Paper
from .serializers import ReviewSerializer
from reviews.models import Review
from conferences.models import Conference
from . import permissions

class ReviewListView(generics.ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsReviewerOrPaperOwner]

    def get_queryset(self):
        conf = self.kwargs.get('conf')
        pk = self.kwargs.get('pk')
        queryset = Review.objects.filter(paper__id=pk).select_related('paper', 'user')
        return queryset
    
    def get_view_name(self):
        return "List of Reviews for a Paper"

class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsReviewOwner]

    def get_queryset(self):
        conf = self.kwargs.get('conf')
        pk = self.kwargs.get('pk')
        review_pk = self.kwargs.get('review_pk')
        if conf is None or pk is None or review_pk is None:
            raise NotFound("Conference, paper, or review not found.")
        return Review.objects.filter(paper__id=pk).select_related('paper', 'user')

    def get_object(self):
        queryset = self.get_queryset()
        obj = generics.get_object_or_404(queryset, pk=self.kwargs['review_pk'])
        return obj

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def get_view_name(self):
        return "Detail of Review for a Paper"

class ReviewCreateView(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, permissions.CanSubmitReview]

    def perform_create(self, serializer):
        conf = self.kwargs.get('conf')
        pk = self.kwargs.get('pk')
        if conf is None or pk is None:
            raise NotFound("Conference or paper not found.")
        
        conference = get_object_or_404(Conference, acronym=conf)
        paper = get_object_or_404(Paper, pk=pk)
        reviewer = self.request.user
        review_queryset = Review.objects.filter(paper=paper, user=reviewer)

        if review_queryset.exists():
            raise ValidationError("You have already reviewed this paper!")
        
        serializer.save(paper=paper, user=reviewer)
    
    def get_view_name(self):
        return "Submit Review for Paper"