"""Views."""

from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import (ListView,
                                  CreateView,
                                  UpdateView,
                                  DeleteView)


from task_manager.mixins import (SuccessMessageMixin,
                                 RedirectOnProtectedMixin)
from task_manager.apps.user.mixins import UserLoginRequiredMixin

from .forms import StatusForm
from .models import Status


class ListStatusView(UserLoginRequiredMixin, ListView):
    """List of statuses view."""

    model = Status
    ordering = 'pk'
    template_name = 'status/list.html'


class CreateStatusView(SuccessMessageMixin,
                       UserLoginRequiredMixin,
                       CreateView):
    """Create status view."""

    model = Status
    form_class = StatusForm
    template_name = 'status/create.html'
    success_url = reverse_lazy('statuses')
    success_message = _('Status was created')


class UpdateStatusView(SuccessMessageMixin,
                       UserLoginRequiredMixin,
                       UpdateView):
    """Update status view."""

    model = Status
    form_class = StatusForm
    template_name = 'status/update.html'
    success_url = reverse_lazy('statuses')
    success_message = _('Status was updated')


class DeleteStatusView(UserLoginRequiredMixin,
                       RedirectOnProtectedMixin,
                       SuccessMessageMixin,
                       DeleteView):
    """Delete status view"""

    model = Status
    template_name = 'status/delete.html'
    success_url = reverse_lazy('statuses')
    success_message = _('Status was deleted.')
    denied_url = reverse_lazy('statuses')
    denied_message = _('Status in use. You can not delete it.')
