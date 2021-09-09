"""Filters."""

import django_filters
from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Task
from label.models import Label


class TaskFilter(django_filters.FilterSet):
    """Task filter."""

    self_tasks = django_filters.BooleanFilter(widget=forms.CheckboxInput,
                                              label=_('Only my tasks'),
                                              method='choose_user_as_author')
    labels = django_filters.ModelChoiceFilter(queryset=Label.objects.all().order_by('pk'))

    class Meta:
        model = Task
        fields = (
            'author',
            'executor',
            'labels',
            'status',
            'self_tasks',
        )

    def choose_user_as_author(self, queryset, name, value):
        if value:
            return queryset.filter(author_id=self.request.user.id)
        return queryset
