"""Forms."""

from django import forms
from django.utils.translation import gettext

from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    """User form."""

    # password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        """Meta class."""

        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
        )


class CreateUserForm(forms.ModelForm):
    """Create user form."""

    username = forms.CharField(
        label=gettext('Username'),
        widget=forms.TextInput(
            attrs={'placeholder': ''}
        )
    )

    first_name = forms.CharField(
        label=gettext('First name'),
        widget=forms.TextInput(
            attrs={'placeholder': ''}
        ),
    )

    last_name = forms.CharField(
        label=gettext('Last name'),
        widget=forms.TextInput(
            attrs={'placeholder': ''}
        )
    )

    email = forms.EmailField(
        label=gettext('Email'),
        widget=forms.TextInput(
            attrs={'placeholder': 'example@domain.com'}
        ),
        help_text=gettext('I will not check, but I believe that it is working')
    )

    password = forms.CharField(
        label=gettext('Password'),
        widget=forms.PasswordInput(
            attrs={'placeholder': ''}
        ))

    password_confirm = forms.CharField(
        label=gettext('Repeat password'),
        widget=forms.PasswordInput(
            attrs={'placeholder': ''}
        ))

    class Meta:
        """Meta class."""

        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
        )

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
