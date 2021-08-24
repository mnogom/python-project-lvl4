from django.shortcuts import render
from django.views import View
from django.http import HttpResponse

from task_manager import status

from .forms import UserForm
from .selectors import get_all_users
from .services import create_user


class ListUsersView(View):
    def get(self, request):
        print(get_all_users())
        return HttpResponse('страница со списком всех пользователей')


class NewUserView(View):
    def get(self, request):
        # return HttpResponse('страница регистрации нового пользователя (создание)')
        return render(request, 'create.html', {'form': UserForm})

    def post(self, request):

        try:
            something = create_user(request.POST)
        except Exception as exception:
            return render(request,
                          'create.html',
                          {'form': UserForm(request.POST)},
                          status=status.HTTP_400_BAD_REQUEST)
        return HttpResponse('создание пользователя')


class EditUserView(View):
    def get(self, request, pk):
        return HttpResponse(f'страница редактирования пользователя {pk}')

    def post(self, request, pk):
        return HttpResponse(f'обновление пользователя {pk}')


class DeleteUserView(View):
    def get(self, request, pk):
        return HttpResponse(f'страница удаления пользователя {pk}')

    def post(self, request, pk):
        return HttpResponse(f'удаление пользователя {pk}')


class LoginView(View):
    def get(self, request):
        return HttpResponse('страница входа')

    def post(self, request):
        return HttpResponse('аутентификация (вход)')


class LogoutView(View):
    def post(self):
        return HttpResponse('завершение сессии (выход)')
