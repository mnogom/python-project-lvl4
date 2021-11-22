"""Mixins."""

from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.mixins import (AccessMixin,
                                        LoginRequiredMixin,
                                        UserPassesTestMixin)


# class UserLoginRequiredMixin(LoginRequiredMixin):
#     """User login required mixin."""
#
#     def dispatch(self, request, *args, **kwargs):
#         """Dispatch method."""
#
#         if not request.user.is_authenticated:
#             messages.add_message(request=request,
#                                  message=_('You need to login to do this'),
#                                  level=messages.ERROR)
#         return super().dispatch(request, *args, **kwargs)


class UserLoginRequiredMixin(LoginRequiredMixin):
    raise_exception = False

    def dispatch(self, request, *args, **kwargs):
        self.permission_denied_redirect_url = reverse_lazy('login')
        self.permission_denied_message = _('login')
        return super().dispatch(request, *args, **kwargs)


class UserPermissionEditSelfMixin(UserPassesTestMixin):
    raise_exception = False

    def test_func(self):
        if self.request.user.pk != self.kwargs.get('pk'):
            self.permission_denied_redirect_url = reverse_lazy('user:list')
            self.permission_denied_message = _('No permission')
            return False
        return True

    # def get_permission_denied_message(self):
    #     return _('No permission')


# class UserPermissionEditSelfMixin(AccessMixin):
#     """User permission edit only self mixin."""
#
#     def dispatch(self, request, *args, **kwargs):
#         """Dispatch method."""
#
#         if int(request.user.pk) != kwargs.get('pk', None):
#             if self.permission_denied_message:
#                 messages.add_message(request=request,
#                                      message=self.permission_denied_message,
#                                      level=messages.ERROR)
#             return redirect(request.META.get('HTTP_REFERER',
#                                              reverse_lazy('index')))
#         return super().dispatch(request, *args, **kwargs)


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


class UserIsAuthorMixin:
    """Mixin to give permission to author edit only his tasks.

    TODO: make from user pass tests.
    """

    def dispatch(self, request, *args, **kwargs):
        """Dispatch method."""

        task = self.get_object()
        if task.author_id == int(self.request.user.pk):
            return super().dispatch(request, *args, **kwargs)

        messages.add_message(request=request,
                             message=_('Only author can edit task'),
                             level=messages.ERROR)
        return redirect(reverse_lazy('task:list'))
