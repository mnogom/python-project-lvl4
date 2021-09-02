"""Views."""

from django.shortcuts import render, redirect, resolve_url
from django.views import View
from django.views.generic.list import ListView
from django.utils.translation import gettext
from django.contrib import messages


from task_manager import http_status

from .models import User
from .forms import (UserForm,
                    LoginForm)
from .selectors import get_user_by_pk
from .services import (create_user,
                       login_user,
                       logout_user,
                       delete_user,
                       update_user)
from .decorators import (required_login,
                         user_pk_check,
                         required_not_login)


class ListUsersView(ListView):
    """List of users view."""

    model = User
    template_name = 'users.html'


class CreateUserView(View):
    """New user view."""

    @required_not_login
    def get(self, request):
        """Method GET."""

        return render(request=request,
                      template_name='create_user.html',
                      context={'form': UserForm},
                      status=http_status.HTTP_200_OK)

    @required_not_login
    def post(self, request):
        """Method POST."""

        form = create_user(request.POST)
        if form.is_valid():
            messages.add_message(request=request,
                                 level=messages.SUCCESS,
                                 message=gettext('Nice! Now you can login'))
            return redirect(resolve_url('login'))
        return render(request=request,
                      template_name='create_user.html',
                      context={'form': form},
                      status=http_status.HTTP_400_BAD_REQUEST)


class UpdateUserView(View):
    """Edit user view."""

    @required_login
    @user_pk_check
    def get(self, request, pk: int):
        """Method GET."""

        user = get_user_by_pk(pk)
        form = UserForm(instance=user)
        return render(request=request,
                      template_name='edit_user.html',
                      context={'form': form,
                               'user_pk': pk},
                      status=http_status.HTTP_200_OK)

    @required_login
    @user_pk_check
    def post(self, request, pk: int):
        """Method POST."""

        form = update_user(request.POST, pk)
        if form.is_valid():
            messages.add_message(request=request,
                                 level=messages.SUCCESS,
                                 message=gettext('User profile was updated'))
            login_user(request)
            return redirect(resolve_url('update_user', pk=pk))

        return render(request=request,
                      template_name='edit_user.html',
                      context={'form': form,
                               'user_pk': pk},
                      status=http_status.HTTP_400_BAD_REQUEST)


class DeleteUserView(View):
    """Delete user view."""

    @required_login
    @user_pk_check
    def get(self, request, pk: int):
        """Method GET."""

        user = get_user_by_pk(pk)
        return render(request=request,
                      template_name='delete_user.html',
                      context={'user': user},
                      status=http_status.HTTP_200_OK)

    @required_login
    @user_pk_check
    def post(self, request, pk: int):
        """Method POST."""

        delete_user(pk=pk)
        messages.add_message(request=request,
                             level=messages.SUCCESS,
                             message=gettext('User was deleted'))
        return redirect(resolve_url('index'))


class LoginView(View):
    """Login view."""

    @required_not_login
    def get(self, request):
        """Method GET."""

        return render(request=request,
                      template_name='login_user.html',
                      context={'form': LoginForm},
                      status=http_status.HTTP_200_OK)

    @required_not_login
    def post(self, request):
        """Method POST."""

        if login_user(request):
            return redirect(resolve_url('index'))

        messages.add_message(request=request,
                             level=messages.WARNING,
                             message=gettext('Username or password (or both) are wrong'))
        return render(request=request,
                      template_name='login_user.html',
                      context={'form': LoginForm},
                      status=http_status.HTTP_400_BAD_REQUEST)


class LogoutView(View):
    """Logout view."""

    @required_login
    def post(self, request):
        """Method POST."""

        logout_user(request)
        return redirect(resolve_url('index'))
