"""Models."""

from django.db import models


class Task(models.Model):
    name = models.CharField(max_length=300, blank=False, null=False, unique=True)
    description = models.CharField(max_length=300, blank=True, null=False)
    author = models.ForeignKey('auth.User', on_delete=models.PROTECT, related_name='author')
    executor = models.ForeignKey('auth.User', on_delete=models.PROTECT, related_name='executor')
    created_at = models.DateField(auto_now_add=True, editable=False)
