from django.contrib import admin

from .models import EditorConference, ReviewerConference, ReviewerPaper

admin.site.register(EditorConference)
admin.site.register(ReviewerConference)
admin.site.register(ReviewerPaper)