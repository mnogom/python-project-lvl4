"""Mixins."""

from django.contrib import messages
from django.db.models.deletion import ProtectedError
from django.shortcuts import redirect


class CheckIfObjectInUseMixin:
    """Mixin to add message and make redirect if
    object for delete is used by another objects.
    """

    object_in_use_message = None
    object_in_use_url = None

    def redirect_on_protected_error(self):
        """Add message to response and get redirect url."""

        if self.object_in_use_message:
            messages.error(self.request,
                           message=self.object_in_use_message)
        return redirect(self.object_in_use_url)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
        except ProtectedError:
            return self.redirect_on_protected_error()
        success_url = self.get_success_url()
        return redirect(success_url)


class SuccessMessageMixin:
    """Mixin to add success message to response
    if View call 'get_success_url' method.

    Default SuccessMessageMixin add message only if form is valid.
    This one can add message to any View that called 'get_success_url' method
    """

    success_url = None
    success_message = None

    def get_success_url(self):
        """Get success url method."""

        if self.success_message:
            messages.success(request=self.request,
                             message=self.success_message)
        return self.success_url
