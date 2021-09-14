"""Mixins."""

from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from django.utils.translation import gettext_lazy as _


class OnlyAuthorCanEditTaskMixin:
    def dispatch(self, request, *args, **kwargs):
        task = self.get_object()
        if task.author_id == int(self.request.user.pk):
            return super().dispatch(request, *args, **kwargs)

        messages.add_message(request=request,
                             message=_('Only author can delete task'),
                             level=messages.ERROR)
        return redirect(reverse_lazy('tasks'))
