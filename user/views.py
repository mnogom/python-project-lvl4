"""Views."""

from django.shortcuts import render, redirect, resolve_url
from django.views import View
from django.views.generic.list import ListView
from django.utils.translation import gettext
from django.contrib import messages

from django.contrib.auth.models import User

from task_manager import status

from .forms import (EditUserForm,
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


    def get(self, request, *args, **kwargs):
        return super().get(self, request, *args, **kwargs)


class NewUserView(View):
    """New user view."""

    @required_not_login
    def get(self, request):
        """Method GET."""

        return render(request=request,
                      template_name='create.html',
                      context={'form': EditUserForm},
                      status=status.HTTP_200_OK)

    @required_not_login
    def post(self, request):
        """Method POST."""

        user = create_user(request.POST)
        if user is not None:
            messages.add_message(request=request,
                                 level=messages.SUCCESS,
                                 message=gettext('Nice! Now you can login'))
            return redirect(resolve_url('login'))
        else:
            return render(request=request,
                          template_name='create.html',
                          context={'form': EditUserForm(request.POST)},
                          status=status.HTTP_400_BAD_REQUEST)


class EditUserView(View):
    """Edit user view."""

    @required_login
    @user_pk_check
    def get(self, request, pk: int):
        """Method GET."""

        user = get_user_by_pk(pk)
        form = EditUserForm(instance=user)
        return render(request=request,
                      template_name='edit.html',
                      context={'form': form,
                               'user_pk': pk},
                      status=status.HTTP_200_OK)

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
                      template_name='edit.html',
                      context={'form': form,
                               'user_pk': pk},
                      status=status.HTTP_400_BAD_REQUEST)


class DeleteUserView(View):
    """Delete user view."""

    @required_login
    @user_pk_check
    def get(self, request, pk: int):
        """Method GET."""

        user = get_user_by_pk(pk)
        return render(request=request,
                      template_name='delete.html',
                      context={'user': user},
                      status=status.HTTP_200_OK)

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
                      template_name='login.html',
                      context={'form': LoginForm},
                      status=status.HTTP_200_OK)

    @required_not_login
    def post(self, request):
        """Method POST."""

        login_success = login_user(request)
        if login_success:
            return redirect(resolve_url('index'))

        messages.add_message(request=request,
                             level=messages.WARNING,
                             message=gettext('Username or password (or both) are wrong'))
        return redirect(resolve_url('login'))


class LogoutView(View):
    """Logout view."""

    @required_login
    def post(self, request):
        """Method POST."""

        logout_user(request)
        return redirect(resolve_url('index'))
