"""Fields."""

from django import forms
from django.utils.translation import gettext_lazy as _

from status.selectors import get_all_statuses
from user.models import User


name_field = forms.CharField(
    label=_('Name'),
    widget=forms.TextInput(
        attrs={'placeholder': ''}
    )
)

description_field = forms.CharField(
    label=_('Description'),
    required=False,
    widget=forms.Textarea(
        attrs={'placeholder': ''}
    )
)

status_field = forms.ModelChoiceField(
    label=_('Status'),
    queryset=get_all_statuses().order_by('name'),
)

executor_field = forms.ModelChoiceField(
    label=_('Executor'),
    queryset=User.objects.all().order_by('first_name'),
    to_field_name='pk'
)
