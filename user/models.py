"""Models."""

from django.contrib.auth.models import User


# Make field email for User unique
User._meta.get_field('email')._unique = True
