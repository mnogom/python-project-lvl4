"""Fields."""

from django import forms
from django.utils.translation import gettext_lazy as _


password1_field = forms.CharField(
    label=_('Password'),
    widget=forms.PasswordInput(
        attrs={'placeholder': ''}
    )
)

password2_field = forms.CharField(
    label=_('Repeat password'),
    widget=forms.PasswordInput(
        attrs={'placeholder': ''}
    )
)