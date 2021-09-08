"""Filters."""

import django_filters

from .models import Task
from label.models import Label


class TaskFilter(django_filters.FilterSet):  # TODO: return tasks if user is author. Do with checkbox!
    labels = django_filters.ModelChoiceFilter(queryset=Label.objects.all().order_by('pk'))

    class Meta:
        model = Task
        fields = (
            'author',
            'executor',
            'labels',
            'status',
        )
