"""Fields."""

from django import forms
from django.utils.translation import gettext_lazy as _


username_field = forms.CharField(
    # label=_('Username'),
    widget=forms.TextInput(
        attrs={'placeholder': '',
               'id': 'id_username'}
    ),
)

first_name_field = forms.CharField(
    # label=_('First name'),
    widget=forms.TextInput(
        attrs={'placeholder': ''}
    )
)

last_name_field = forms.CharField(
    # label=_('Last name'),
    widget=forms.TextInput(
        attrs={'placeholder': ''}
    )
)

email_field = forms.EmailField(
    # label=_('Email'),
    widget=forms.TextInput(
        attrs={'placeholder': 'example@domain.com'},
    ),
    help_text=_('I will not check, but I believe that it is working')
)

password1 = forms.CharField(
    label=_('Password'),
    widget=forms.PasswordInput(
        attrs={'placeholder': ''}
    )
)

password2 = forms.CharField(
    label=_('Repeat password'),
    widget=forms.PasswordInput(
        attrs={'placeholder': ''}
    )
)