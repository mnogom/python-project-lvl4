"""Views."""

from django.urls import reverse_lazy
from django.views.generic import (DetailView,
                                  CreateView,
                                  UpdateView,
                                  DeleteView)
from django.utils.translation import gettext_lazy as _

from task_manager.mixins import (SuccessMessageMixin,
                                 RedirectOnProtectedMixin)
from task_manager.apps.user.mixins import UserLoginRequiredMixin

from django_filters.views import FilterView

from .forms import TaskForm
from .models import Task
from .mixins import (OnlyAuthorCanEditTaskMixin,
                     ValidateTaskMixin)
from .filters import TaskFilter


class ListTaskView(UserLoginRequiredMixin,
                   FilterView):
    """List tasks filter view."""

    model = Task
    ordering = 'pk'
    filterset_class = TaskFilter
    template_name = 'task/tasks.html'


class CreateTaskView(SuccessMessageMixin,
                     UserLoginRequiredMixin,
                     ValidateTaskMixin,
                     CreateView):
    """Create task view."""

    model = Task
    form_class = TaskForm
    template_name = 'task/create_task.html'
    success_url = reverse_lazy('tasks')
    success_message = _('Task was created')


class UpdateTaskView(SuccessMessageMixin,
                     UserLoginRequiredMixin,
                     OnlyAuthorCanEditTaskMixin,
                     ValidateTaskMixin,
                     UpdateView):
    """Update task view."""

    model = Task
    form_class = TaskForm
    template_name = 'task/update_task.html'
    success_url = reverse_lazy('tasks')
    success_message = _('Task was updated')


class DeleteTaskView(SuccessMessageMixin,
                     UserLoginRequiredMixin,
                     RedirectOnProtectedMixin,
                     OnlyAuthorCanEditTaskMixin,
                     DeleteView):
    """Delete task view."""

    model = Task
    template_name = 'task/delete_task.html'
    success_url = reverse_lazy('tasks')
    success_message = _('Task was deleted')
    denied_url = reverse_lazy('tasks')
    denied_message = _('Task in use. You can not delete it.')


class TaskView(UserLoginRequiredMixin,
               DetailView):
    """Task view."""

    template_name = 'task/task.html'
    model = Task
