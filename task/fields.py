"""Fields."""

from django import forms
from django.utils.translation import gettext_lazy as _

from status.selectors import get_all_statuses
from user.selectors import get_all_users


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

from django.contrib.auth.models import User

executor_field = forms.ModelChoiceField(
    label=_('Executor'),
    queryset=get_all_users().order_by('username'),
    to_field_name='pk'
)
