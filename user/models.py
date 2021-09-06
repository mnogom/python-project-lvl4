"""Models."""

# TODO: Read about User model
# https://docs.djangoproject.com/en/3.2/topics/auth/customizing/#using-a-custom-user-model-when-starting-a-project

from django.contrib.auth.models import User


# Make field email for User unique.
User._meta.get_field('email')._unique = True


# Overwrite '__str__' method.
def get_full_name(self):
    return self.get_full_name()


User.add_to_class('__str__', get_full_name)
