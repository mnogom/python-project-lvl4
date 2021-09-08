"""Models."""

from django.db import models


class Task(models.Model):
    name = models.CharField(max_length=300, blank=False, null=False, unique=True)
    description = models.TextField(blank=True, null=False)
    author = models.ForeignKey('user.User', on_delete=models.PROTECT, related_name='author')
    executor = models.ForeignKey('user.User', on_delete=models.PROTECT, related_name='executor')
    status = models.ForeignKey('status.Status', on_delete=models.PROTECT, related_name='status')
    labels = models.ManyToManyField('label.Label', through='TaskLabel')
    created_at = models.DateField(auto_now_add=True, editable=False)


class TaskLabel(models.Model):
    task = models.ForeignKey('task.Task', on_delete=models.CASCADE)
    label = models.ForeignKey('label.Label', on_delete=models.PROTECT)
