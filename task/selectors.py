"""Selectors."""

from django.core.exceptions import ObjectDoesNotExist

from .models import Task
from .exceptions import TaskDoesNotExist


def get_all_tasks():
    """Get all users.

    :return: QuerySet of Users
    """

    return Task.objects.all().order_by('pk')


def get_task_by_pk(pk: int):
    """Get user by primal key

    :param pk: user primal key
    :return: User object
    """

    try:
        return Task.objects.get(pk=pk)
    except ObjectDoesNotExist:
        raise TaskDoesNotExist
