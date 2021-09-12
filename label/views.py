"""Views."""

from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import (ListView,
                                  CreateView,
                                  UpdateView,
                                  DeleteView)

from task_manager.mixins import (SuccessMessageMixin,
                                 RedirectOnProtectedMixin)
from user.mixins import UserLoginRequiredMixin

from .forms import LabelForm
from .models import Label


class ListLabelView(UserLoginRequiredMixin,
                    ListView):

    model = Label
    template_name = 'labels.html'


class CreateLabelView(SuccessMessageMixin,
                      UserLoginRequiredMixin,
                      CreateView):
    model = Label
    form_class = LabelForm
    template_name = 'create_label.html'
    success_url = reverse_lazy('labels')
    success_message = _('Label was created')


class UpdateLabelView(SuccessMessageMixin,
                      UserLoginRequiredMixin,
                      UpdateView):
    model = Label
    form_class = LabelForm
    template_name = 'update_label.html'
    success_url = reverse_lazy('labels')
    success_message = _('Label was updated')


class DeleteLabelView(SuccessMessageMixin,
                      RedirectOnProtectedMixin,
                      UserLoginRequiredMixin,
                      DeleteView):
    model = Label
    template_name = 'delete_label.html'
    success_url = reverse_lazy('labels')
    success_message = _('Label was deleted')
    denied_url = reverse_lazy('labels')
    denied_message = _('Label in use. You can not delete it.')
