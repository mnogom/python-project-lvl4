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
        attrs={'placeholder': '',
               'id': 'id_first_name'}
    )
)

last_name_field = forms.CharField(
    label=gettext('Last name'),
    widget=forms.TextInput(
        attrs={'placeholder': '',
               'id': 'id_last_name'}
    )
)

email_field = forms.EmailField(
    label=gettext('Email'),
    widget=forms.TextInput(
        attrs={'placeholder': 'example@domain.com',
               'id': 'id_email'},
    ),
    help_text=gettext('I will not check, but I believe that it is working')
)

password_field = forms.CharField(
    label=gettext('Password'),
    widget=forms.PasswordInput(
        attrs={'placeholder': '',
               'id': 'id_password1'}
    )
)

password_confirm_field = forms.CharField(
    label=gettext('Password'),
    widget=forms.PasswordInput(
        attrs={'placeholder': '',
               'id': 'id_password2'}
    )
)