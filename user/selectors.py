"""Selectors."""

from django.core.exceptions import ObjectDoesNotExist

from .exceptions import UserDoesNotExist
from .models import User


def get_all_users():
    """Get all users.

    :return: QuerySet of Users
    """

    return User.objects.all()


def get_user_by_pk(pk: int):
    """Get user by primal key

    :param pk: user primal key
    :return: User object
    """

    try:
        return User.objects.get(pk=pk)
    except ObjectDoesNotExist:
        raise UserDoesNotExist
