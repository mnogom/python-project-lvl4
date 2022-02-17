"""Mixins."""

from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.mixins import (AccessMixin,
                                        LoginRequiredMixin,
                                        UserPassesTestMixin)


class UserLoginRequiredMixin(LoginRequiredMixin):
    """User login required mixin."""

    raise_exception = False

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            self.permission_denied_message = _('You need to login to do this')
            self.permission_denied_redirect_url = reverse_lazy('login')
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class UserPermissionEditSelfMixin(UserPassesTestMixin):
    """User permission edit only self mixin."""

    raise_exception = False

    def test_func(self):
        if self.request.user.pk:
            if self.request.user.pk != self.kwargs.get('pk'):
                self.permission_denied_redirect_url = reverse_lazy('user:list')

                if self.__class__.__name__.lower().startswith('update'):
                    self.permission_denied_message = _('You have no permission to edit users')
                elif self.__class__.__name__.lower().startswith('delete'):
                    self.permission_denied_message = _('You have no permission to delete users')
                return False
        return True


class UserLoginUnRequiredMixin(AccessMixin):
    """User login required mixin."""

    already_login_message = _('You are already logged in')

    def dispatch(self, request, *args, **kwargs):
        """Dispatch method."""

        if request.user.is_authenticated:
            if self.already_login_message:
                messages.warning(request=request,
                                 message=self.already_login_message)
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

        messages.warning(request=request,
                         message=_('Only author can edit task'))
        return redirect(reverse_lazy('task:list'))
