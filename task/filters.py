"""Filters."""

import django_filters
from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Task
from user.models import User
from label.models import Label
from status.models import Status


class TaskFilter(django_filters.FilterSet):
    """Task filter."""
    widget = ''
    self_tasks = django_filters.BooleanFilter(label=_('Only my tasks'),
                                              method='choose_user_as_author',
                                              widget=forms.CheckboxInput(attrs={'id': 'id_self_tasks'}))
    label = django_filters.ModelChoiceFilter(queryset=Label.objects.all().order_by('pk'),
                                             label=_('Label'),
                                             method='choose_label',
                                             widget=forms.Select(attrs={'id': 'id_label'}))
    author = django_filters.ModelChoiceFilter(queryset=User.objects.all().order_by('pk'),
                                              label=_('Author'),
                                              widget=forms.Select(attrs={'id': 'id_author'}))
    executor = django_filters.ModelChoiceFilter(queryset=User.objects.all().order_by('pk'),
                                                label=_('Executor'),
                                                widget=forms.Select(attrs={'id': 'id_executor'}))
    status = django_filters.ModelChoiceFilter(queryset=Status.objects.all().order_by('pk'),
                                              label=_('Status'),
                                              widget=forms.Select(attrs={'id': 'id_status'}))

    class Meta:
        model = Task
        fields = (
            'author',
            'executor',
            'label',
            'status',
            'self_tasks',
        )

    def choose_user_as_author(self, queryset, name, value):
        if value:
            return queryset.filter(author_id=self.request.user.id)
        return queryset

    def choose_label(self, queryset, name, value):
        if value:
            return queryset.filter(tasklabel__label_id=value)
