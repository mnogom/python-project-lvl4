from django.shortcuts import render
from django.views import View
from django.http import HttpResponse

from user.decorators import required_login

class ListTaskView(View):
    # @required_login
    def get(self, *args, **kwargs):
        return HttpResponse('страница со списком всех задач')


class CreateTaskView(View):
    # @required_login
    def get(self, *args, **kwargs):
        return HttpResponse('страница создания задачи')

    # @required_login
    def post(self, *args, **kwargs):
        return HttpResponse('создание новой задачи')


class UpdateTaskView(View):
    # @required_login
    def get(self, *args, **kwargs):
        return HttpResponse('страница редактирования задачи')

    # @required_login
    def post(self, *args, **kwargs):
        return HttpResponse('обновление задачи')


class DeleteTaskView(View):
    # @required_login
    def get(self, *args, **kwargs):
        return HttpResponse('страница удаления задачи')

    # @required_login
    def post(self, *args, **kwargs):
        return HttpResponse('удаление задачи')


class TaskView(View):
    # @required_login
    def get(self, *args, **kwargs):
        return HttpResponse('страница просмотра задачи')
