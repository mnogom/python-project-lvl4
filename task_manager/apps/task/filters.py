"""Filters."""

import django_filters
from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Task
from task_manager.apps.label.models import Label


class TaskFilter(django_filters.FilterSet):
    """Task filter."""

    self_tasks = django_filters.BooleanFilter(label=_('Only my tasks'),
                                              method='choose_user_as_author',
                                              widget=forms.CheckboxInput)
    label = django_filters.ModelChoiceFilter(queryset=Label.objects.all().order_by('pk'),
                                             label=_('Label'),
                                             method='choose_label')

    class Meta:
        """Meta class."""

        model = Task
        fields = (
            'author',
            'executor',
            'label',
            'status',
            'self_tasks',
        )

    def choose_user_as_author(self, queryset, name, value):
        """Filter by checkbox 'self_tasks'."""

        if value:
            return queryset.filter(author_id=self.request.user.id)
        return queryset

    def choose_label(self, queryset, name, value):
        """Filter by single label."""

        if value:
            return queryset.filter(tasklabel__label_id=value)
