"""Selectors."""

from django.core.exceptions import ObjectDoesNotExist

from .models import User
from .exceptions import UserDoesNotExist


def get_all_users():
    """Get all users.

    :return: QuerySet of Users
    """

    return User.objects.all().order_by('pk')


def get_user_by_pk(pk: int):
    """Get user by primal key

    :param pk: user primal key
    :return: User object
    """

    try:
        return User.objects.get(pk=pk)
    except ObjectDoesNotExist:
        raise UserDoesNotExist
