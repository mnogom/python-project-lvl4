"""Mixins."""

from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        UserPassesTestMixin)
from django.contrib import messages

from django.shortcuts import redirect


class UserLoginRequiredMixin(LoginRequiredMixin):
    """User login required mixin."""

    def dispatch(self, request, *args, **kwargs):
        self.permission_denied_message = _('You need to login to do this')
        self.permission_denied_redirect_url = reverse_lazy('login')
        return super().dispatch(request, *args, **kwargs)

    def handle_no_permission(self):
        return super().handle_no_permission()


class UserPermissionModifySelfMixin(UserPassesTestMixin):
    """User permission edit only self mixin."""

    def dispatch(self, request, *args, **kwargs):
        self.permission_denied_redirect_url = reverse_lazy('user:list')
        if self.__class__.__name__.lower().startswith('update'):
            self.permission_denied_message = _('You have no permission to edit users')
        elif self.__class__.__name__.lower().startswith('delete'):
            self.permission_denied_message = _('You have no permission to delete users')
        return super().dispatch(request, *args, **kwargs)

    def test_func(self):
        return self.request.user.pk == self.kwargs.get('pk')


class UserIsAuthorMixin(UserPassesTestMixin):
    """Mixin to give permission to author edit only his tasks."""

    def dispatch(self, request, *args, **kwargs):
        self.permission_denied_message = _('Only author can edit task')
        self.permission_denied_redirect_url = reverse_lazy('task:list')
        return super().dispatch(request, *args, **kwargs)

    def test_func(self):
        return self.get_object().author == self.request.user


class UserPermissionDeniedMessageMixin:

    def handle_no_permission(self):
        if self.permission_denied_message:
            messages.error(request=self.request,
                           message=self.permission_denied_message)
        return redirect(self.permission_denied_redirect_url)
