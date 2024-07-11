from django.shortcuts import get_object_or_404

from rest_framework import permissions

from conferences.models import Conference
from linkers.models import EditorConference, ReviewerConference

class CanAddToConference(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            conf_acronym = view.kwargs.get('conf')
            conference = get_object_or_404(Conference, acronym=conf_acronym)
            return EditorConference.objects.filter(user=request.user, conference=conference).exists()
        return False