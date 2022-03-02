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
    model = User
    ordering = 'pk'
    template_name = 'user/list.html'


class CreateUserView(SuccessMessageMixin,
                     CreateView):
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
    model = User
    form_class = UserCreateForm
    template_name = 'user/update.html'
    success_url = reverse_lazy('user:list')
    success_message = _('User profile was updated')

    def post(self, request, *args, **kwargs):
        """Force re-login user after user profile update."""

        response = super().post(request, *args, **kwargs)
        login_user(request)
        return response


class DeleteUserView(SuccessMessageMixin,
                     CheckIfObjectInUseMixin,
                     UserPermissionDeniedMessageMixin,
                     UserPermissionModifySelfMixin,
                     UserLoginRequiredMixin,
                     DeleteView):
    model = User
    template_name = 'user/delete.html'
    success_message = _('User was deleted')
    success_url = reverse_lazy('user:list')
    object_in_use_url = reverse_lazy('user:list')
    object_in_use_message = _('User in use. You can not delete it.')


class LoginUserView(SuccessMessageMixin,
                    LoginView):
    template_name = 'user/login.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('index')
    success_message = _('You are logged in')


class LogoutUserView(SuccessMessageMixin,
                     UserPermissionDeniedMessageMixin,
                     UserLoginRequiredMixin,
                     LogoutView):
    success_message = _('You are logged out')

    def dispatch(self, request, *args, **kwargs):
        """Disable GET method for logout view
        and add success_message to response

        Default dispatch method in LogoutView don't call 'get_success_message'
        and don't filter request methods.
        """

        if request.method == 'GET':
            return super().http_method_not_allowed(request, *args, **kwargs)
        self.get_success_url()
        return super().dispatch(request, *args, **kwargs)


class UserView(UserPermissionDeniedMessageMixin,
               UserLoginRequiredMixin,
               DetailView):
    template_name = 'user/read.html'
    model = User
