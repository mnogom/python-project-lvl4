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

from .forms import LabelForm
from .models import Label


class ListLabelView(UserPermissionDeniedMessageMixin,
                    UserLoginRequiredMixin,
                    ListView):
    """List label view."""

    model = Label
    ordering = 'pk'
    template_name = 'label/list.html'


class CreateLabelView(SuccessMessageMixin,
                      UserPermissionDeniedMessageMixin,
                      UserLoginRequiredMixin,
                      CreateView):
    """Create label view."""

    model = Label
    form_class = LabelForm
    template_name = 'label/create.html'
    success_url = reverse_lazy('label:list')
    success_message = _('Label was created')


class UpdateLabelView(SuccessMessageMixin,
                      UserPermissionDeniedMessageMixin,
                      UserLoginRequiredMixin,
                      UpdateView):
    """Update label view."""

    model = Label
    form_class = LabelForm
    template_name = 'label/update.html'
    success_url = reverse_lazy('label:list')
    success_message = _('Label was updated')


class DeleteLabelView(SuccessMessageMixin,
                      CheckIfObjectInUseMixin,
                      UserPermissionDeniedMessageMixin,
                      UserLoginRequiredMixin,
                      DeleteView):
    """Delete label view."""

    model = Label
    template_name = 'label/delete.html'
    success_url = reverse_lazy('label:list')
    success_message = _('Label was deleted')
    object_in_use_url = reverse_lazy('label:list')
    object_in_use_message = _('Label in use. You can not delete it.')
