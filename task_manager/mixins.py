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
        """get success url method."""

        if self.success_message:
            messages.add_message(request=self.request,
                                 message=self.success_message,
                                 level=messages.SUCCESS)
        return self.success_url


class RedirectOnProtectedMixin:
    """Mixin to redirect if object is protected."""

    denied_url = None
    denied_message = None

    def delete(self, request, *args, **kwargs):
        """Delete method."""

        self.object = self.get_object()
        try:
            self.object.delete()
        except ProtectedError:
            if self.denied_message:
                messages.set_level(request, messages.ERROR)
                messages.add_message(request=request,
                                     message=self.denied_message,
                                     level=messages.ERROR)
            return redirect(self.denied_url or reverse_lazy('index'))
        success_url = self.get_success_url()
        return HttpResponseRedirect(success_url)
