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
                                 CheckIfObjectInUseMixin)

from .models import User
from .forms import UserCreateForm
from .services import login_user
from .mixins import (UserLoginRequiredMixin,
                     UserPermissionModifySelfMixin,
                     UserPermissionDeniedMessageMixin)


class ListUsersView(ListView):
    """List of users view."""

    model = User
    ordering = 'pk'
    template_name = 'user/list.html'


class CreateUserView(SuccessMessageMixin,
                     CreateView):
    """New user view."""

    model = User
    form_class = UserCreateForm
    template_name = 'user/create.html'
    success_url = reverse_lazy('login')
    success_message = _('User profile was successfully created')


class UpdateUserView(SuccessMessageMixin,
                     UserPermissionDeniedMessageMixin,
                     UserPermissionModifySelfMixin,
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
                     CheckIfObjectInUseMixin,
                     UserPermissionDeniedMessageMixin,
                     UserPermissionModifySelfMixin,
                     UserLoginRequiredMixin,
                     DeleteView):
    """Delete user view."""

    model = User
    template_name = 'user/delete.html'
    success_message = _('User was deleted')
    success_url = reverse_lazy('user:list')
    object_in_use_url = reverse_lazy('user:list')
    object_in_use_message = _('User in use. You can not delete it.')


class LoginUserView(SuccessMessageMixin,
                    LoginView):
    """Login view.
    """

    template_name = 'user/login.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('index')
    success_message = _('You are logged in')


class LogoutUserView(SuccessMessageMixin,
                     UserPermissionDeniedMessageMixin,
                     UserLoginRequiredMixin,
                     LogoutView):
    """Logout view."""

    success_message = _('You are logged out')
    http_method_names = ['POST', ]

    def dispatch(self, request, *args, **kwargs):
        """Dispatch method."""

        if request.method == 'GET':
            return super().http_method_not_allowed(request, *args, **kwargs)
        self.get_success_url()
        return super().dispatch(request, *args, **kwargs)


class UserView(UserPermissionDeniedMessageMixin,
               UserLoginRequiredMixin,
               DetailView):
    """User view."""

    template_name = 'user/read.html'
    model = User
