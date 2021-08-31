"""Fields."""

from django import forms
from django.utils.translation import gettext


name_field = forms.CharField(
    max_length=300,
    label=gettext('Name'),
    required=True,
    widget=forms.TextInput(
        attrs={'placeholder': '',
               'id': 'id_name'}
    )
)

description_field = forms.CharField(
    label=gettext('Description'),
    required=False,
    widget=forms.Textarea(
        attrs={'placeholder': '',
               'id': 'id_description'}
    )
)
