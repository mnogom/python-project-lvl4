"""Views."""

from django.urls import reverse_lazy
from django.views.generic import (DetailView,
                                  ListView,
                                  CreateView,
                                  UpdateView,
                                  DeleteView)
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.views import (LoginView,
                                       LogoutView)

from task_manager.mixins import (SuccessMessageMixin,
                                 PermissionDeniedMixin,
                                 RedirectOnProtectedMixin)

from .models import User
from .forms import UserCreateForm
from .services import login_user
from .mixins import (UserLoginRequiredMixin,
                     UserPermissionEditSelfMixin)


class ListUsersView(ListView):
    """List of users view."""

    model = User
    ordering = 'pk'
    template_name = 'user/list.html'


class CreateUserView(SuccessMessageMixin,
                     CreateView):
    """New user view."""
    # TODO: [hexlet-check]
    #  To pass hexlet check
    #  you must have access to registration page if
    #  you are already logged in
    #  if it fix you can add 'UserLoginUnRequiredMixin'

    model = User
    form_class = UserCreateForm
    template_name = 'user/create.html'
    success_url = reverse_lazy('login')
    success_message = _('User profile was successfully created')


class UpdateUserView(SuccessMessageMixin,
                     PermissionDeniedMixin,
                     UserPermissionEditSelfMixin,
                     UserLoginRequiredMixin,
                     UpdateView):
    """Edit user view."""

    model = User
    form_class = UserCreateForm
    template_name = 'user/update.html'
    success_url = reverse_lazy('user:list')
    success_message = _('User profile was updated')

    def post(self, request, *args, **kwargs):
        """Auto log in on success updating user."""

        response = super().post(request, *args, **kwargs)
        login_user(request)
        return response


class DeleteUserView(SuccessMessageMixin,
                     RedirectOnProtectedMixin,
                     PermissionDeniedMixin,
                     UserPermissionEditSelfMixin,
                     UserLoginRequiredMixin,
                     DeleteView):
    """Delete user view."""

    model = User
    template_name = 'user/delete.html'
    success_message = _('User was deleted')
    success_url = reverse_lazy('user:list')


class LoginUserView(SuccessMessageMixin,
                    LoginView):
    """Login view.

    TODO: don't show 'applied status' at fields in form
      when user input is not valid to login
    """

    template_name = 'user/login.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('index')
    success_message = _('You are logged in')


class LogoutUserView(SuccessMessageMixin,
                     PermissionDeniedMixin,
                     UserLoginRequiredMixin,
                     LogoutView):
    """Logout view."""

    success_message = _('You are logged out')
    http_method_names = ['POST', ]

    def dispatch(self, request, *args, **kwargs):
        """Dispatch method."""

        if request.method == 'GET':
            # TODO: [fix] make error page
            return super().http_method_not_allowed(request, *args, **kwargs)
        self.get_success_url()
        return super().dispatch(request, *args, **kwargs)


class UserView(PermissionDeniedMixin,
               UserLoginRequiredMixin,
               DetailView):
    """User view."""

    template_name = 'user/sample.html'
    model = User
