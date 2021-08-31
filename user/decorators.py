from django.shortcuts import redirect, resolve_url
from django.utils.translation import gettext
from django.contrib import messages


def _back_url(request, default='index'):
    _url = request.META.get('HTTP_REFERER')
    return _url if _url else default


def required_login(fn):
    def inner(obj, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.add_message(request=request,
                                 level=messages.ERROR,
                                 message=gettext('You need to login'))
            return redirect('login')
        return fn(obj, request, *args, **kwargs)
    return inner


def user_pk_check(fn):
    def inner(obj, request, *args, **kwargs):
        if int(request.user.pk) != kwargs.get('pk'):
            messages.add_message(request=request,
                                 level=messages.ERROR,
                                 message=gettext('You have no permission edit other users.'))
            return redirect(_back_url(request, 'users'))
        return fn(obj, request, *args, **kwargs)
    return inner


def required_not_login(fn):
    def inner(obj, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.add_message(request,
                                 level=messages.INFO,
                                 message=gettext('You already logged in'))
            return redirect(_back_url(request, 'index'))
        return fn(obj, request, *args, **kwargs)
    return inner
