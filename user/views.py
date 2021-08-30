"""Views."""

from django.shortcuts import render, redirect, resolve_url
from django.views import View
from django.views.generic.list import ListView
from django.utils.translation import gettext
from django.http import HttpResponse
from django.contrib import messages

from django.contrib.auth.models import User

from task_manager import status

from .forms import (UpdateUserForm,
                    CreateUserForm,
                    LoginForm)
from .selectors import (get_all_users,
                        get_user_by_pk)
from .services import (create_user,
                       login_user,
                       logout_user,
                       delete_user)
from .exceptions import UserFormIsNotValid


class ListUsersView(ListView):
    """List of users view."""

    model = User
    template_name = 'users.html'


class NewUserView(View):
    """New user view."""

    def get(self, request):
        """Method GET."""

        if request.user.is_authenticated:
            return redirect(resolve_url('update_user', pk=request.user.pk))

        return render(request=request,
                      template_name='create.html',
                      context={'form': CreateUserForm},
                      status=status.HTTP_200_OK)

    def post(self, request):
        """Method POST."""

        try:
            create_user(request.POST)
            messages.add_message(request=request,
                                 level=messages.SUCCESS,
                                 message=gettext('Nice! Now you can login'))
            return redirect(resolve_url('login'))
        except UserFormIsNotValid:
            return render(request=request,
                          template_name='create.html',
                          context={'form': CreateUserForm(request.POST)},
                          status=status.HTTP_400_BAD_REQUEST)


class EditUserView(View):
    """Edit user view."""

    def get(self, request, pk: int):
        """Method GET."""

        user = get_user_by_pk(pk)
        return render(request=request,
                      template_name='edit.html',
                      context={'form': UpdateUserForm(instance=user),
                               'user_pk': pk},
                      status=status.HTTP_200_OK)

    def post(self, request, pk: int):
        """Method POST."""

        return HttpResponse(f'обновление пользователя {pk}')


class DeleteUserView(View):
    """Delete user view."""

    def get(self, request, pk: int):
        """Method GET."""

        return render(request=request,
                      template_name='delete.html',
                      context={'user': get_user_by_pk(pk)},
                      status=status.HTTP_200_OK)

    def post(self, request, pk: int):
        """Method POST."""

        delete_user(request, pk)
        messages.add_message(request=request,
                             level=messages.SUCCESS,
                             message=gettext('User was deleted'))
        return redirect(resolve_url('index'))


class LoginView(View):
    """Login view."""

    def get(self, request):
        """Method GET."""

        if request.user.is_authenticated:
            return redirect(resolve_url('update_user', pk=request.user.pk))

        return render(request=request,
                      template_name='login.html',
                      context={'form': LoginForm},
                      status=status.HTTP_200_OK)

    def post(self, request):
        """Method POST."""

        login_user(request)
        return redirect(resolve_url('index'))


class LogoutView(View):
    """Logout view."""

    def post(self, request):
        """Method POST."""

        logout_user(request)
        return redirect(resolve_url('index'))
