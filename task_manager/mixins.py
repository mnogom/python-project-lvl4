"""Mixins."""

from django.contrib import messages
from django.db.models.deletion import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect


class SuccessMessageMixin:
    success_url = None
    success_message = None

    def get_success_url(self):
        if self.success_message:
            messages.add_message(request=self.request,
                                 message=self.success_message,
                                 level=messages.SUCCESS)
        return self.success_url


class RedirectOnProtectedMixin:
    denied_url = None
    denied_message = None

    def delete(self, request, *args, **kwargs):
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
