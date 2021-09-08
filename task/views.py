"""Views."""

from django.urls import reverse_lazy
from django.views.generic import (DetailView,
                                  ListView,
                                  CreateView,
                                  UpdateView,
                                  DeleteView)
from django.utils.translation import gettext_lazy as _

from task_manager.mixins import (SuccessMessageMixin,
                                 RedirectOnProtectedMixin)
from user.mixins import UserLoginRequiredMixin

from .forms import TaskForm
from .models import Task
from .mixins import OnlyAuthorCanDeleteMixin


class ListTaskView(UserLoginRequiredMixin,
                   ListView):
    model = Task
    template_name = 'tasks.html'


class CreateTaskView(SuccessMessageMixin,
                     UserLoginRequiredMixin,
                     CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'create_task.html'
    success_url = reverse_lazy('tasks')
    success_message = _('Task was created')

    def form_valid(self, form):
        form.set_author(self.request.user.pk)
        return super().form_valid(form)


class UpdateTaskView(SuccessMessageMixin,
                     UserLoginRequiredMixin,
                     UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'update_task.html'
    success_url = reverse_lazy('tasks')
    success_message = _('Task was updated')

    def form_valid(self, form):  # TODO: make way to add author easier
        form.set_author(self.request.user.pk)
        return super().form_valid(form)


class DeleteTaskView(SuccessMessageMixin,
                     UserLoginRequiredMixin,
                     RedirectOnProtectedMixin,
                     OnlyAuthorCanDeleteMixin,
                     DeleteView):

    model = Task
    template_name = 'delete_task.html'
    success_url = reverse_lazy('tasks')
    success_message = _('Task was deleted')
    denied_url = reverse_lazy('tasks')
    denied_message = _('Task in use. You can not delete it.')


class TaskView(UserLoginRequiredMixin,
               DetailView):
    template_name = 'task.html'
    model = Task
