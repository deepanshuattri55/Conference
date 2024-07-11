from django.shortcuts import get_object_or_404
from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied

from papers.models import Paper
from linkers.models import ReviewerPaper

class IsReviewerOrPaperOwner(permissions.BasePermission):
    """
    Custom permission to allow only reviewers or paper owners to view the reviews.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.paper.user == request.user or obj.user == request.user

class IsReviewOwner(permissions.BasePermission):
    """
    Custom permission to allow only the review owner to perform actions on the review.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

class CanSubmitReview(permissions.BasePermission):
    """
    Custom permission to allow only the reviewer assigned to submit a review.
    """
    def has_permission(self, request, view):
        pk = view.kwargs.get('pk')
        if pk is None:
            raise PermissionDenied("Paper ID (pk) is required.")
        
        paper = get_object_or_404(Paper, pk=pk)
        user = request.user
        
        if ReviewerPaper.objects.filter(paper=paper, user=user).exists():
            return True
        return False