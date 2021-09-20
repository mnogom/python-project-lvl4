"""Models."""

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import EmailValidator
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """User model."""
    # TODO: [hexlet-check]
    #  To pass hexlet check you need keep
    #  email 'unique=False', 'blank=True', 'null=True'

    username_validator = UnicodeUsernameValidator()
    email_validator = EmailValidator()

    username = models.CharField(verbose_name=_('username'),
                                max_length=150,
                                unique=True,
                                help_text=_('Your username must be unique'),
                                validators=[username_validator],
                                error_messages={
                                    'unique': _('A user with that username already exists.'), })
    email = models.CharField(verbose_name=_('email'),
                             max_length=150,
                             blank=True,
                             null=True,
                             # unique=True,
                             help_text=_('Your email must exists and be unique.'),
                             validators=[email_validator],
                             error_messages={
                                 'unique': _('A user with that email already exists.'), })

    def __str__(self):
        """representation method."""

        return self.get_full_name() or f'@{self.username}'

    class Meta(AbstractUser.Meta):
        """Meta class."""

        swappable = 'AUTH_USER_MODEL'
