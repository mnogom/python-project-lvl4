"""Views."""

from django.urls import reverse_lazy
from django.views.generic import (DetailView,
                                  CreateView,
                                  UpdateView,
                                  DeleteView)
from django.utils.translation import gettext_lazy as _

from task_manager.mixins import (CheckIfObjectInUseMixin,
                                 SuccessMessageMixin)
from task_manager.apps.user.mixins import (UserLoginRequiredMixin,
                                           UserPermissionDeniedMessageMixin,
                                           UserIsAuthorMixin)

from django_filters.views import FilterView

from .forms import TaskForm
from .models import Task
from .filters import TaskFilter


class ListTaskView(UserPermissionDeniedMessageMixin,
                   UserLoginRequiredMixin,
                   FilterView):
    model = Task
    ordering = 'pk'
    filterset_class = TaskFilter
    template_name = 'task/list.html'


class CreateTaskView(SuccessMessageMixin,
                     UserPermissionDeniedMessageMixin,
                     UserLoginRequiredMixin,
                     CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'task/create.html'
    success_url = reverse_lazy('task:list')
    success_message = _('Task was created')

    def form_valid(self, form):
        form.set_author(self.request.user.pk)
        return super().form_valid(form)


class UpdateTaskView(SuccessMessageMixin,
                     UserPermissionDeniedMessageMixin,
                     UserLoginRequiredMixin,
                     UserIsAuthorMixin,
                     UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'task/update.html'
    success_url = reverse_lazy('task:list')
    success_message = _('Task was updated')


class DeleteTaskView(SuccessMessageMixin,
                     UserPermissionDeniedMessageMixin,
                     UserLoginRequiredMixin,
                     CheckIfObjectInUseMixin,
                     UserIsAuthorMixin,
                     DeleteView):
    model = Task
    template_name = 'task/delete.html'
    success_url = reverse_lazy('task:list')
    success_message = _('Task was deleted')
    denied_url = reverse_lazy('task:list')
    denied_message = _('Task in use. You can not delete it.')


class TaskView(UserPermissionDeniedMessageMixin,
               UserLoginRequiredMixin,
               DetailView):
    template_name = 'task/read.html'
    model = Task
