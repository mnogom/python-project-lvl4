"""Mixins."""

from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.mixins import (AccessMixin,
                                        LoginRequiredMixin)


class UserLoginRequiredMixin(LoginRequiredMixin):
    """User login required mixin."""

    def dispatch(self, request, *args, **kwargs):
        """Dispatch method."""

        if not request.user.is_authenticated:
            messages.add_message(request=request,
                                 message=_('You need to login to do this'),
                                 level=messages.ERROR)
        return super().dispatch(request, *args, **kwargs)


class UserPermissionEditSelfMixin(AccessMixin):
    """User permission edit only self mixin."""

    def dispatch(self, request, *args, **kwargs):
        """Dispatch method."""

        if int(request.user.pk) != kwargs.get('pk', None):
            if self.permission_denied_message:
                messages.add_message(request=request,
                                     message=self.permission_denied_message,
                                     level=messages.ERROR)
            return redirect(request.META.get('HTTP_REFERER',
                                             reverse_lazy('index')))
        return super().dispatch(request, *args, **kwargs)


class UserLoginUnRequiredMixin(AccessMixin):
    """User login required mixin."""

    already_login_message = _('You are already logged in')

    def dispatch(self, request, *args, **kwargs):
        """Dispatch method."""

        if request.user.is_authenticated:
            if self.already_login_message:
                messages.add_message(request=request,
                                     message=self.already_login_message,
                                     level=messages.WARNING)
            return redirect(request.META.get('HTTP_REFERER',
                                             reverse_lazy('index')))
        return super().dispatch(request, *args, **kwargs)