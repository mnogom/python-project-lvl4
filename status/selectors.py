"""Selectors."""

from django.core.exceptions import ObjectDoesNotExist

from .exceptions import StatusDoesNotExist
from .models import Status


def get_all_statuses():
    """Get all statuses.

    :return: QuerySet of Statuses
    """

    return Status.objects.all().order_by('pk')


def get_status_by_pk(pk: int):
    """Get status by primal key

    :param pk: status primal key
    :return: Status object
    """

    try:
        return Status.objects.get(pk=pk)
    except ObjectDoesNotExist:
        raise StatusDoesNotExist
