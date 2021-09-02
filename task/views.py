from django.shortcuts import render
from django.views import View
from django.http import HttpResponse

from task_manager import http_status
from user.decorators import required_login

from .forms import StatusForm


class ListTaskView(View):
    # @required_login
    def get(self, request, *args, **kwargs):
        return HttpResponse('страница со списком всех задач')


class CreateTaskView(View):
    # @required_login
    def get(self, request, *args, **kwargs):
        return render(request=request,
                      template_name='create_task.html',
                      context={'form': StatusForm},
                      status=http_status.HTTP_200_OK)

    # @required_login
    def post(self, request, *args, **kwargs):
        return HttpResponse('создание новой задачи')


class UpdateTaskView(View):
    # @required_login
    def get(self, request, *args, **kwargs):
        return HttpResponse('страница редактирования задачи')

    # @required_login
    def post(self, request, *args, **kwargs):
        return HttpResponse('обновление задачи')


class DeleteTaskView(View):
    # @required_login
    def get(self, request, *args, **kwargs):
        return HttpResponse('страница удаления задачи')

    # @required_login
    def post(self, request, *args, **kwargs):
        return HttpResponse('удаление задачи')


class TaskView(View):
    # @required_login
    def get(self, request, *args, **kwargs):
        return HttpResponse('страница просмотра задачи')
