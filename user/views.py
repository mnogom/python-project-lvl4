"""Views."""

from django.shortcuts import render
from django.views import View
from django.http import HttpResponse

from task_manager import status

from .forms import (UserForm,
                    CreateUserForm)
from .selectors import (get_all_users,
                        get_user_by_pk)
from .services import create_user


class ListUsersView(View):
    """List of users view."""

    def get(self, request):
        """Method GET."""

        print(get_all_users())
        return HttpResponse('страница со списком всех пользователей')


class NewUserView(View):
    """New user view."""

    def get(self, request):
        """Method GET."""

        return render(request=request,
                      template_name='create.html',
                      context={'form': CreateUserForm},
                      status=status.HTTP_200_OK)

    def post(self, request):
        """Method POST."""

        try:
            user = create_user(request.POST)
        except Exception as exception:
            return render(request=request,
                          template_name='create.html',
                          context={'form': CreateUserForm(request.POST)},
                          status=status.HTTP_400_BAD_REQUEST)
        return HttpResponse('создание пользователя')


class EditUserView(View):
    """Edit user view."""

    def get(self, request, pk: int):
        """Method GET."""

        user = get_user_by_pk(pk)

        return render(request=request,
                      template_name='edit.html',
                      context={'form': UserForm(instance=user)},
                      status=status.HTTP_200_OK)

    def post(self, request, pk: int):
        """Method POST."""

        return HttpResponse(f'обновление пользователя {pk}')


class DeleteUserView(View):
    """Delete user view."""

    def get(self, request, pk: int):
        """Method GET."""

        return HttpResponse(f'страница удаления пользователя {pk}')

    def post(self, request, pk: int):
        """Method POST."""

        return HttpResponse(f'удаление пользователя {pk}')


class LoginView(View):
    """Login view."""

    def get(self, request):
        """Method GET."""

        return HttpResponse('страница входа')

    def post(self, request):
        """Method POST."""

        return HttpResponse('аутентификация (вход)')


class LogoutView(View):
    """Logout view."""

    def post(self):
        """Method POST."""

        return HttpResponse('завершение сессии (выход)')
