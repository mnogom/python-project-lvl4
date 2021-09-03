from django.shortcuts import render, redirect, resolve_url
from django.views import View
from django.views.generic import ListView
from django.contrib import messages
from django.utils.translation import gettext


from task_manager import http_status
from user.decorators import required_login

from .forms import TaskForm
from .services import (create_task,
                       update_task,
                       delete_task)
from .selectors import get_task_by_pk
from .models import Task
from .decorators import user_is_author_check


class ListTaskView(ListView):

    model = Task
    template_name = 'tasks.html'

    @required_login
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class CreateTaskView(View):
    @required_login
    def get(self, request, *args, **kwargs):
        form = TaskForm(initial={'author_pk': request.user.pk})
        return render(request=request,
                      template_name='create_task.html',
                      context={'form': form},
                      status=http_status.HTTP_200_OK)

    @required_login
    def post(self, request, *args, **kwargs):

        author_pk = request.user.pk
        form = create_task(status_data=request.POST,
                           author_pk=author_pk)
        if form.is_valid():
            messages.add_message(request=request,
                                 level=messages.SUCCESS,
                                 message=gettext('Task was created'))
            return redirect(resolve_url('tasks'))

        return render(request=request,
                      template_name='create_task.html',
                      context={'form': form},
                      status=http_status.HTTP_400_BAD_REQUEST)


class UpdateTaskView(View):
    @required_login
    @user_is_author_check
    def get(self, request, pk, *args, **kwargs):
        task = get_task_by_pk(pk)
        form = TaskForm(instance=task)
        return render(request=request,
                      template_name='edit_task.html',
                      context={'form': form,
                               'task_pk': pk},
                      status=http_status.HTTP_200_OK)

    @required_login
    @user_is_author_check
    def post(self, request, pk, *args, **kwargs):
        form = update_task(request.POST, pk)
        if form.is_valid():
            messages.add_message(request=request,
                                 level=messages.SUCCESS,
                                 message=gettext('Task was updated'))
            return redirect(resolve_url('tasks'))
        return render(request=request,
                      template_name='edit_task.html',
                      context={'form': form,
                               'task_pk': pk},
                      status=http_status.HTTP_400_BAD_REQUEST)


class DeleteTaskView(View):
    @required_login
    @user_is_author_check
    def get(self, request, pk, *args, **kwargs):
        task = get_task_by_pk(pk)
        return render(request=request,
                      template_name='delete_task.html',
                      context={'task': task},
                      status=http_status.HTTP_200_OK)

    @required_login
    @user_is_author_check
    def post(self, request, pk, *args, **kwargs):
        task = delete_task(pk)
        if task:
            messages.add_message(request=request,
                                 level=messages.SUCCESS,
                                 message=gettext('Task was deleted'))
        else:
            messages.add_message(request=request,
                                 level=messages.ERROR,
                                 message=gettext('Project in use'))
        return redirect(resolve_url('tasks'))


class TaskView(View):
    @required_login
    def get(self, request, pk, *args, **kwargs):
        task = get_task_by_pk(pk)
        return render(request=request,
                      template_name='task.html',
                      context={'task': task},
                      status=http_status.HTTP_200_OK)
