"""Decorators."""

from django.shortcuts import redirect, resolve_url
from django.utils.translation import gettext
from django.contrib import messages

from task_manager.shortcuts import back_url

from .selectors import get_task_by_pk


def user_is_author_check(fn):
    def inner(obj, request, *args, **kwargs):
        author_pk = get_task_by_pk(kwargs.get('pk')).author_id
        if int(request.user.pk) != author_pk:
            messages.add_message(request=request,
                                 level=messages.ERROR,
                                 message=gettext('You have permission edit only tasks where you is author.'))
            return redirect(back_url(request, 'tasks'))
        return fn(obj, request, *args, **kwargs)
    return inner
