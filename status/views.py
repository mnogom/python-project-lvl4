"""Views."""

from django.urls import reverse_lazy
from django.utils.translation import gettext
from django.views.generic import (ListView,
                                  CreateView,
                                  UpdateView,
                                  DeleteView)

from task_manager.mixins import TMSuccessMessageMixin
from user.mixins import UserLoginRequiredMixin

from .forms import StatusForm
from .models import Status


class ListStatusView(UserLoginRequiredMixin, ListView):
    """List of users view."""

    model = Status
    template_name = 'statuses.html'


class CreateStatusView(TMSuccessMessageMixin,
                       UserLoginRequiredMixin,
                       CreateView):

    model = Status
    form_class = StatusForm
    template_name = 'create_status.html'
    success_url = reverse_lazy('statuses')
    success_message = gettext('Status was created')


class UpdateStatusView(TMSuccessMessageMixin,
                       UserLoginRequiredMixin,
                       UpdateView):

    model = Status
    form_class = StatusForm
    template_name = 'update_status.html'
    success_url = reverse_lazy('statuses')
    success_message = gettext('Status was updated')


class DeleteStatusView(TMSuccessMessageMixin,
                       UserLoginRequiredMixin,
                       DeleteView):

    model = Status
    template_name = 'delete_status.html'
    success_url = reverse_lazy('statuses')
    success_message = gettext('Status was deleted')
