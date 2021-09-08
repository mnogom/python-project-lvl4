"""Forms."""

from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from .models import User
from .fields import (password1_field,
                     password2_field)


class UserForm(ModelForm):
    """Create user form."""

    password1 = password1_field
    password2 = password2_field

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
            self.add_error('password2', _('Passwords does not match'))
        return cleaned_data

    def save(self, **kwargs):
        """Save user method."""

        user = super().save(**kwargs)
        user.set_password(self.cleaned_data["password1"])
        user.save()
        return user
