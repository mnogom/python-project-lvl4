"""Fields."""

from django import forms
from django.utils.translation import gettext

from status.selectors import get_all_statuses
from user.selectors import get_all_users


name_field = forms.CharField(
    label=gettext('Name'),
    widget=forms.TextInput(
        attrs={'placeholder': '',
               'id': 'id_name'}
    ),
)

description_field = forms.CharField(
    label=gettext('Description'),
    required=False,
    widget=forms.Textarea(
        attrs={'placeholder': '',
               'id': 'id_description'}
    )
)


status_field = forms.ModelChoiceField(
    queryset=get_all_statuses().order_by('name')
)

from django.contrib.auth.models import User
executor_field = forms.ModelChoiceField(
    queryset=get_all_users().order_by('username')
)


# status_field = forms.Select(
#     choices=CHOICES
# )