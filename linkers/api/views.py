from django.shortcuts import get_object_or_404

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from . import serializers, permissions, pagination
from linkers import models
from papers.models import Paper
from conferences.models import Conference
from user_app.models import CustomUser

class BaseConferenceCreateView(generics.CreateAPIView):
    def create(self, request, *args, **kwargs):
        conf_acronym = self.kwargs['conf']
        conference = get_object_or_404(models.Conference, acronym=conf_acronym)

        email = request.data.get('email')
        if not email:
            return Response({"detail": "Email field is required."}, status=status.HTTP_400_BAD_REQUEST)

        user, created = CustomUser.objects.get_or_create(email=email)

        instance = self.get_queryset().model()
        instance.conference.set([conference])
        instance.user.set([user])
        instance.save()

        if created:
            return Response({"detail": "User created and added to the conference."}, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail": "User added to the conference."}, status=status.HTTP_201_CREATED)

class EditorConferenceListView(generics.ListAPIView):
    serializer_class = serializers.EditorConferenceListSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = pagination.EditorConferenceCursorPagination

    def get_queryset(self):
        user = self.request.user
        queryset = models.EditorConference.objects.filter(user=user)
        return queryset

    def get_view_name(self):
        return "Editors of Conference - List"

class EditorConferenceCreateView(BaseConferenceCreateView):
    serializer_class = serializers.EditorConferenceCreateSerializer
    permission_classes = [permissions.CanAddToConference]

    def get_queryset(self):
        return models.EditorConference.objects.all()
    
    def get_view_name(self):
        return "Add Editor to Conference"

class ReviewerConferenceListView(generics.ListAPIView):
    serializer_class = serializers.ReviewerConferenceListSerializer
    permission_classes = [IsAuthenticated]
    ination_class = pagination.ReviewerConferenceCursorPagination

    def get_queryset(self):
        user = self.request.user
        queryset = models.ReviewerConference.objects.filter(user=user)
        return queryset

    def get_view_name(self):
        return "Reviewers of Conference - List"

class ReviewerConferenceCreateView(BaseConferenceCreateView):
    serializer_class = serializers.ReviewerConferenceCreateSerializer
    permission_classes = [permissions.CanAddToConference]

    def get_queryset(self):
        return models.ReviewerConference.objects.all()
    
    def get_view_name(self):
        return "Add Reviewers to Conference"

class ReviewerPaperListView(generics.ListAPIView):
    serializer_class = serializers.ReviewerPaperListSerializer
    permission_classes = [IsAuthenticated]
    ination_class = pagination.ReviewerPaperCursorPagination

    def get_queryset(self):
        conf_acronym = self.kwargs['conf']
        conference = get_object_or_404(Conference, acronym=conf_acronym)

        papers_in_conference = Paper.objects.filter(conference=conference)
        user = self.request.user
        reviewer_papers = []

        for paper in papers_in_conference:
            if models.ReviewerPaper.objects.filter(user=user, paper=paper).exists():
                reviewer_paper = models.ReviewerPaper.objects.get(user=user, paper=paper)
                reviewer_papers.append(reviewer_paper)
        
        return reviewer_papers
    
    def get_view_name(self):
        return "Reviewers of Paper - List"


class ReviewerPaperCreateView(generics.CreateAPIView):
    serializer_class = serializers.ReviewerPaperCreateSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        conf_acronym = self.kwargs['conf']
        paper_pk = self.kwargs['pk']
        conference = get_object_or_404(Conference, acronym=conf_acronym)
        reviewer_conferences = models.ReviewerConference.objects.filter(conference=conference)
        
        reviewers = []
        for reviewer_conf in reviewer_conferences:
            reviewers.extend(reviewer_conf.user.all())

        context['choices'] = [(reviewer.email, reviewer.email) for reviewer in reviewers]
        context['paper_pk'] = paper_pk
        return context
    
    def perform_create(self, serializer):
        paper = get_object_or_404(Paper, pk=self.kwargs['pk'])

        user_email = serializer.validated_data.get('reviewers')
        user = get_object_or_404(CustomUser, email=user_email)

        serializer.save(paper=paper, user=user, paper_pk=self.kwargs['pk'])
    
    def get_view_name(self):
        return "Add Reviewer to Paper"