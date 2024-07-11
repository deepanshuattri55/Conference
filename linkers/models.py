from django.db import models
from django.contrib.auth import get_user_model

from conferences.models import Conference
from papers.models import Paper

class EditorConference(models.Model):
    user = models.ManyToManyField(get_user_model())
    conference = models.ManyToManyField(Conference)

    def __str__(self) -> str:
        user_names = ", ".join([user.first_name for user in self.user.all()])
        conference_titles = ", ".join([conf.title for conf in self.conference.all()])
        return f'{user_names} <-> {conference_titles} [Editor]'

class ReviewerConference(models.Model):
    user = models.ManyToManyField(get_user_model())
    conference = models.ManyToManyField(Conference)

    def __str__(self) -> str:
        user_names = ", ".join([user.first_name for user in self.user.all()])
        conference_titles = ", ".join([conf.title for conf in self.conference.all()])
        return f'{user_names} <-> {conference_titles} [Reviewer]'

class ReviewerPaper(models.Model):
    user = models.ManyToManyField(get_user_model())
    paper = models.ManyToManyField(Paper)

    def __str__(self) -> str:
        user_names = ", ".join([user.first_name for user in self.user.all()])
        paper_titles = ", ".join([paper.title for paper in self.paper.all()])
        return f'{user_names} <-> {paper_titles} [Review]'