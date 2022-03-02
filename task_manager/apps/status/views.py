"""Views."""

from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import (ListView,
                                  CreateView,
                                  UpdateView,
                                  DeleteView)

from task_manager.mixins import (CheckIfObjectInUseMixin,
                                 SuccessMessageMixin)
from task_manager.apps.user.mixins import (UserLoginRequiredMixin,
                                           UserPermissionDeniedMessageMixin)

from .forms import StatusForm
from .models import Status


class ListStatusView(UserPermissionDeniedMessageMixin,
                     UserLoginRequiredMixin,
                     ListView):
    model = Status
    ordering = 'pk'
    template_name = 'status/list.html'


class CreateStatusView(SuccessMessageMixin,
                       UserPermissionDeniedMessageMixin,
                       UserLoginRequiredMixin,
                       CreateView):
    model = Status
    form_class = StatusForm
    template_name = 'status/create.html'
    success_url = reverse_lazy('status:list')
    success_message = _('Status was created')


class UpdateStatusView(SuccessMessageMixin,
                       UserPermissionDeniedMessageMixin,
                       UserLoginRequiredMixin,
                       UpdateView):
    model = Status
    form_class = StatusForm
    template_name = 'status/update.html'
    success_url = reverse_lazy('status:list')
    success_message = _('Status was updated')


class DeleteStatusView(SuccessMessageMixin,
                       CheckIfObjectInUseMixin,
                       UserPermissionDeniedMessageMixin,
                       UserLoginRequiredMixin,
                       DeleteView):
    model = Status
    template_name = 'status/delete.html'
    success_url = reverse_lazy('status:list')
    success_message = _('Status was deleted.')
    object_in_use_url = reverse_lazy('status:list')
    object_in_use_message = _('Status in use. You can not delete it.')
