"""Mixins."""

from django.contrib import messages
from django.db.models.deletion import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect


class SuccessMessageMixin:
    """Mixin to add success message to response."""

    success_url = None
    success_message = None

    def get_success_url(self):
        """Get success url method."""

        if self.success_message:
            messages.add_message(request=self.request,
                                 message=self.success_message,
                                 level=messages.SUCCESS)
        return self.success_url


class ErrorHandlerMixin:
    def handle_no_permission(self):
        if self.permission_denied_message:
            messages.add_message(request=self.request,
                                 message=self.permission_denied_message,
                                 level=messages.ERROR)
            return HttpResponseRedirect(self.permission_denied_redirect_url)
        return super().handle_no_permission()


class RedirectOnProtectedMixin:
    """Mixin to redirect if object is protected."""

    denied_url = None
    denied_message = None

    def delete(self, request, *args, **kwargs):
        """Delete method."""

        self.object = self.get_object()
        # TODO: Research: https://github.com/jazzband/django-silk -- calculate SQL speed
        try:
            self.object.delete()
        except ProtectedError:
            if self.denied_message:
                messages.set_level(request, messages.ERROR)  # TODO: messages.error
                messages.add_message(request=request,
                                     message=self.denied_message,
                                     level=messages.ERROR)
            return redirect(self.denied_url or reverse_lazy('index'))
        success_url = self.get_success_url()
        return HttpResponseRedirect(success_url)


# TODO: keep it
# class ExceptionMixin(AccessMixin):
#     def get_permission_denied_message(self):
#         pass
#     def handle_no_permission(self):
#         pass
