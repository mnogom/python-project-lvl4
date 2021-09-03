"""Fields."""

from django import forms
from django.utils.translation import gettext


username_field = forms.CharField(
    label=gettext('Username'),
    widget=forms.TextInput(
        attrs={'placeholder': '',
               'id': 'id_username'}
    ),
)

first_name_field = forms.CharField(
    label=gettext('First name'),
    widget=forms.TextInput(
        attrs={'placeholder': ''}
    )
)

last_name_field = forms.CharField(
    label=gettext('Last name'),
    widget=forms.TextInput(
        attrs={'placeholder': ''}
    )
)

email_field = forms.EmailField(
    label=gettext('Email'),
    widget=forms.TextInput(
        attrs={'placeholder': 'example@domain.com'},
    ),
    help_text=gettext('I will not check, but I believe that it is working')
)

password1 = forms.CharField(
    label=gettext('Password'),
    widget=forms.PasswordInput(
        attrs={'placeholder': ''}
    )
)

password2 = forms.CharField(
    label=gettext('Repeat password'),
    widget=forms.PasswordInput(
        attrs={'placeholder': ''}
    )
)