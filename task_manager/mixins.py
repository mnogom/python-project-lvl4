"""Mixins."""

from django.contrib import messages
from django.db.models.deletion import ProtectedError
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.shortcuts import redirect

MESSAGES_ON_PROTECT_DELETE = {
    'User': _('User in use. You can not delete it.'),
    'Label': _('Label in use. You can not delete it.'),
    'Status': _('Status in use. You can not delete it.'),
}
REDIRECT_ON_PROTECT_DELETE = {
    'User': reverse_lazy('user:list'),
    'Label': reverse_lazy('label:list'),
    'Status': reverse_lazy('status:list'),
}


class RedirectOnProtectedMixin:
    """Mixin to redirect if object is protected.

    TODO: 1. вынести сообщение и урл во вьюшку
        2. поробовать отвязать от  handle no permission, чтобы сохранить порядок миксинов
        3. CheckIfObjectInUseMixin ?
    """

    denied_url = None

    def delete(self, request, *args, **kwargs):
        """Delete method."""

        self.object = self.get_object()

        try:
            self.object.delete()
        except ProtectedError:
            self.permission_denied_message = MESSAGES_ON_PROTECT_DELETE.get(
                self.model.__name__,
                '')
            self.permission_denied_redirect_url = REDIRECT_ON_PROTECT_DELETE.get(
                self.model.__name__,
                reverse_lazy('index'))
            return super().handle_no_permission()
        success_url = self.get_success_url()
        return redirect(success_url)


class SuccessMessageMixin:
    """Mixin to add success message to response."""

    success_url = None
    success_message = None

    def get_success_url(self):
        """Get success url method."""

        if self.success_message:
            messages.success(request=self.request,
                             message=self.success_message)
        return self.success_url


class PermissionDeniedMessageMixin:
    """TODO: look up success message mixin"""

    # def get_denied_url(self):
    #     messages.error(request=self.request,
    #                    message=self.denied_message)
    #     return self.denied_url

    def handle_no_permission(self):
        if self.permission_denied_message:
            messages.error(request=self.request,
                           message=self.permission_denied_message)
        return redirect(self.permission_denied_redirect_url)
