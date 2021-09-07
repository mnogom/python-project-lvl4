"""Mixins."""

from django.contrib import messages


class TMSuccessMessageMixin:
    success_url = None
    success_message = None

    def get_success_url(self):
        if self.success_message:
            messages.add_message(request=self.request,
                                 message=self.success_message,
                                 level=messages.SUCCESS)
        return self.success_url
