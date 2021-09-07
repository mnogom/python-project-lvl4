"""Forms."""

from django.forms import ModelForm

from .models import User
from .fields import (username_field,
                     first_name_field,
                     last_name_field,
                     email_field,
                     password1,
                     password2)


class UserForm(ModelForm):
    """Create user form."""

    username = username_field
    first_name = first_name_field
    last_name = last_name_field
    email = email_field
    password1 = password1
    password2 = password2

    class Meta:
        """Meta class."""

        model = User
        fields = ('username',
                  'first_name',
                  'last_name',
                  'email',
                  'password1',)

    def clean(self):
        """Clean method."""

        cleaned_data = super().clean()

        password1 = cleaned_data.get('password1', None)
        password2 = cleaned_data.get('password2', None)
        if password1 != password2:
            self.add_error('password2', 'Password doesn\'t match')
        return cleaned_data

    def save(self, **kwargs):
        """Save user method."""

        user = super().save(**kwargs)
        user.set_password(self.cleaned_data["password1"])
        user.save()
        return user
