"""Views."""

from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import (ListView,
                                  CreateView,
                                  UpdateView,
                                  DeleteView)
# from django.contrib.messages.views import SuccessMessageMixin

from task_manager.mixins import RedirectOnProtectedMixin, SuccessMessageMixin
from task_manager.apps.user.mixins import UserLoginRequiredMixin

from .forms import LabelForm
from .models import Label


class ListLabelView(UserLoginRequiredMixin,
                    ListView):
    """List label view."""

    model = Label
    ordering = 'pk'
    template_name = 'label/list.html'


class CreateLabelView(SuccessMessageMixin,
                      UserLoginRequiredMixin,
                      CreateView):
    """Create label view."""

    model = Label
    form_class = LabelForm
    template_name = 'label/create.html'
    success_url = reverse_lazy('label:list')
    success_message = _('Label was created')


class UpdateLabelView(SuccessMessageMixin,
                      UserLoginRequiredMixin,
                      UpdateView):
    """Update label view."""

    model = Label
    form_class = LabelForm
    template_name = 'label/update.html'
    success_url = reverse_lazy('label:list')
    success_message = _('Label was updated')


class DeleteLabelView(SuccessMessageMixin,
                      RedirectOnProtectedMixin,
                      UserLoginRequiredMixin,
                      DeleteView):
    """Delete label view."""

    model = Label
    template_name = 'label/delete.html'
    success_url = reverse_lazy('label:list')
    success_message = _('Label was deleted')
    denied_url = reverse_lazy('label:list')
    denied_message = _('Label in use. You can not delete it.')
