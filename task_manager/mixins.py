"""Mixins."""

from django.contrib import messages
from django.db.models.deletion import ProtectedError
from django.shortcuts import redirect


class CheckIfObjectInUseMixin:
    """Mixin to redirect if object is protected."""

    object_in_use_message = None
    object_in_use_url = None

    def redirect_on_protected_error(self):
        if self.object_in_use_message:
            messages.error(self.request,
                           message=self.object_in_use_message)
        return redirect(self.object_in_use_url)

    def delete(self, request, *args, **kwargs):
        """Delete method."""

        self.object = self.get_object()
        try:
            self.object.delete()
        except ProtectedError:
            return self.redirect_on_protected_error()
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
