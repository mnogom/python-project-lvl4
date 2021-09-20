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
                                 RedirectOnProtectedMixin)

from .models import User
from .forms import UserForm
from .services import login_user
from .mixins import (UserLoginRequiredMixin,
                     UserLoginUnRequiredMixin,
                     UserPermissionEditSelfMixin)


class ListUsersView(ListView):
    """List of users view."""

    model = User
    ordering = 'pk'
    template_name = 'user/users.html'


class CreateUserView(SuccessMessageMixin,
                     CreateView):
    """New user view."""
    # TODO: [hexlet-check]
    #  To pass hexlet check
    #  you must have access to registration page if
    #  you are already logged in
    #  if it fix you can add 'UserLoginUnRequiredMixin'

    model = User
    form_class = UserForm
    template_name = 'user/create_user.html'
    success_url = reverse_lazy('login')
    success_message = _('User profile was successfully created')


class UpdateUserView(SuccessMessageMixin,
                     UserLoginRequiredMixin,
                     UserPermissionEditSelfMixin,
                     UpdateView):
    """Edit user view."""

    model = User
    form_class = UserForm
    template_name = 'user/update_user.html'
    success_url = reverse_lazy('users')
    success_message = _('User profile was updated')
    permission_denied_message = _('You have no permission to edit users')

    def post(self, request, *args, **kwargs):
        """Auto log in on success updating user."""

        response = super().post(request, *args, **kwargs)
        login_user(request)
        return response


class DeleteUserView(SuccessMessageMixin,
                     UserLoginRequiredMixin,
                     UserPermissionEditSelfMixin,
                     RedirectOnProtectedMixin,
                     DeleteView):
    """Delete user view."""

    model = User
    template_name = 'user/delete_user.html'
    success_message = _('User was deleted')
    permission_denied_message = _('You have no permission to delete users')
    success_url = reverse_lazy('users')
    denied_url = reverse_lazy('users')
    denied_message = _('User in use. You can not delete it.')


class LoginUserView(SuccessMessageMixin,
                    UserLoginUnRequiredMixin,
                    LoginView):
    """Login view."""

    template_name = 'user/login_user.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('index')
    success_message = _('You are logged in')


class LogoutUserView(SuccessMessageMixin,
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


class UserView(UserLoginRequiredMixin, DetailView):
    """User view."""

    template_name = 'user/user.html'
    model = User