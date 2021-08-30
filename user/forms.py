"""Forms."""

from django import forms
from django.utils.translation import gettext

from django.contrib.auth.models import User

from .fields import (username_field,
                     first_name_field,
                     last_name_field,
                     email_field,
                     password_field,
                     password_confirm_field)


class UserForm(forms.ModelForm):
    """User form."""

    username = username_field
    first_name = first_name_field
    last_name = last_name_field
    email = email_field
    password = password_field

    class Meta:
        """Meta class."""

        model = User
        fields = ('username',
                  'first_name',
                  'last_name',
                  'email',
                  'password',)


class CreateUserForm(forms.ModelForm):
    """Create user form."""

    username = username_field
    first_name = first_name_field
    last_name = last_name_field
    email = email_field
    password = password_field
    password_confirm = password_confirm_field

    class Meta:
        """Meta class."""

        model = User
        fields = ('username',
                  'first_name',
                  'last_name',
                  'email',
                  'password',)

    def clean(self):
        """Clean method."""

        cleaned_data = super().clean()
        password = cleaned_data.get('password', None)
        password_confirm = cleaned_data.get('password_confirm', None)
        if password != password_confirm:
            self.add_error('password_confirm', 'Password doesn\'t match')
        return cleaned_data

    def save(self, **kwargs):
        """Save user method."""

        self.cleaned_data.pop('password_confirm')
        User.objects.create_user(**self.cleaned_data)


class LoginForm(forms.ModelForm):
    """Login form"""

    username = username_field
    password = password_field

    class Meta:
        """Meta class."""

        model = User
        fields = ('username',
                  'password',)
