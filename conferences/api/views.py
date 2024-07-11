from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.db.models import Q

from . import serializers, permissions, pagination
from conferences import models

class ConferenceListView(generics.ListAPIView):
    queryset = models.Conference.objects.all()
    serializer_class = serializers.ConferenceSerializer
    pagination_class = pagination.ConferenceLimitOffsetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'acronym', 'venue', 'city', 'country', 'topic']
    ordering_fields = ['title', 'acronym', 'start_date', 'end_date']

    def get_view_name(self):
        return "Conferences List"

class ConferenceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Conference.objects.all()
    serializer_class = serializers.ConferenceSerializer
    lookup_field = 'acronym'
    permission_classes = [permissions.IsConferenceEditor]

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, Q(acronym__iexact=self.kwargs['conf']))
        self.check_object_permissions(self.request, obj)
        return obj
    
    def perform_destroy(self, instance):
        if not self.request.user.is_superuser and not permissions.IsConferenceEditor().has_object_permission(self.request, self, instance):
            raise PermissionDenied("You do not have permission to delete this conference.")
        instance.delete()

    def get_view_name(self):
        return "Conference Detail"

class ConferenceCreateView(generics.CreateAPIView):
    serializer_class = serializers.ConferenceSerializer
    permission_classes = [IsAuthenticated]

    def get_view_name(self):
        return "Create Conference"