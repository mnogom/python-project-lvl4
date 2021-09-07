"""Views."""

from django.urls import reverse_lazy
from django.http import HttpResponseForbidden
from django.views.generic import (DetailView,
                                  ListView,
                                  CreateView,
                                  UpdateView,
                                  DeleteView)
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.views import (LoginView,
                                       LogoutView)

from task_manager.mixins import TMSuccessMessageMixin

from .models import User
from .forms import UserForm
from .services import login_user
from .mixins import (UserLoginRequiredMixin,
                     UserLoginUnRequiredMixin,
                     UserPermissionEditSelfMixin)

class ListUsersView(ListView):
    """List of users view."""

    model = User
    template_name = 'users.html'


class CreateUserView(UserLoginUnRequiredMixin,
                     TMSuccessMessageMixin,
                     CreateView):
    """New user view."""

    model = User
    form_class = UserForm
    template_name = 'create_user.html'
    success_url = reverse_lazy('login')
    success_message = _('User profile was created. Now you can login')


class UpdateUserView(TMSuccessMessageMixin,
                     UserLoginRequiredMixin,
                     UserPermissionEditSelfMixin,
                     UpdateView):
    """Edit user view."""

    model = User
    form_class = UserForm
    template_name = 'update_user.html'
    success_message = _('User profile was updated')
    permission_denied_message = _('You have no permission to edit users')

    def get_success_url(self):
        _ = super().get_success_url()
        return reverse_lazy('user', kwargs={'pk': self.kwargs['pk']})

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        login_user(request)
        return response


class DeleteUserView(TMSuccessMessageMixin,
                     UserLoginRequiredMixin,
                     UserPermissionEditSelfMixin,
                     DeleteView):
    """Delete user view."""

    model = User
    template_name = 'delete_user.html'
    success_message = _('User was deleted')
    permission_denied_message = _('You have no permission to delete users')
    success_url = reverse_lazy('index')


class LoginUserView(UserLoginUnRequiredMixin, LoginView):
    """Login view."""

    template_name = 'login_user.html'
    success_url = reverse_lazy('index')
    redirect_authenticated_user = True


class LogoutUserView(UserLoginRequiredMixin,
                     LogoutView):
    """Logout view."""

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'GET':
            return HttpResponseForbidden('Unexpected method.')  # TODO: make error page
        return super().dispatch(request, *args, **kwargs)


class UserView(UserLoginRequiredMixin, DetailView):
    """User view."""

    template_name = 'user.html'
    model = User
