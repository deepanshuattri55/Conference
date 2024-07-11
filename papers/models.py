from django.db import models
from django.contrib.auth import get_user_model

from conferences.models import Conference
from .consts_ import STATUS_CHOICES

class Paper(models.Model):
    title = models.CharField(max_length=100)
    abstract = models.TextField()
    keywords = models.TextField()
    file = models.FileField(upload_to='conf_papers/')
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, blank=True)
    last_modified = models.DateField(auto_now=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.title}'