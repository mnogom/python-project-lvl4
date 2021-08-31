"""Selectors."""

from django.core.exceptions import ObjectDoesNotExist

from .exceptions import UserDoesNotExist
from .models import Status


def get_all_status():
    """Get all users.

    :return: QuerySet of Users
    """

    return Status.objects.all()


def get_status_by_pk(pk: int):
    """Get user by primal key

    :param pk: user primal key
    :return: User object
    """

    try:
        return Status.objects.get(pk=pk)
    except ObjectDoesNotExist:
        return None
