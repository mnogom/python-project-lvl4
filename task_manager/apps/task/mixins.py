"""Mixins."""

from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from django.utils.translation import gettext_lazy as _


class OnlyAuthorCanEditTaskMixin:
    """Mixin to give permission to author edit only his tasks."""

    def dispatch(self, request, *args, **kwargs):
        """Dispatch method."""

        task = self.get_object()
        if task.author_id == int(self.request.user.pk):
            return super().dispatch(request, *args, **kwargs)

        messages.add_message(request=request,
                             message=_('Only author can edit task'),
                             level=messages.ERROR)
        return redirect(reverse_lazy('tasks'))


class ValidateTaskMixin:
    """Mixin to validate task."""

    def form_valid(self, form):
        """Validate form method.
        TODO: make way to add author easier
        """

        form.set_author(self.request.user.pk)
        return super().form_valid(form)
