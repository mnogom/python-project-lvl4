"""Views."""

from django.urls import reverse_lazy
from django.http import HttpResponseForbidden
from django.views.generic.list import ListView
from django.views.generic.edit import (CreateView,
                                       UpdateView,
                                       DeleteView)
from django.views.generic.detail import DetailView
from django.utils.translation import gettext
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (LoginView,
                                       LogoutView)


from .models import User
from .forms import UserForm
from .services import login_user


class ListUsersView(ListView):
    """List of users view."""

    model = User
    template_name = 'users.html'


class CreateUserView(CreateView):
    """New user view."""

    model = User
    form_class = UserForm
    template_name = 'create_user.html'
    success_url = reverse_lazy('login')


class UpdateUserView(LoginRequiredMixin, UpdateView):
    """Edit user view."""

    model = User
    form_class = UserForm
    template_name = 'update_user.html'

    def get_success_url(self):
        return reverse_lazy('user', kwargs={'pk': self.kwargs['pk']})

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        login_user(request)
        messages.add_message(request=self.request,
                             message=gettext('User profile was updated'),
                             level=messages.SUCCESS)
        return response


class DeleteUserView(DeleteView):
    """Delete user view."""

    model = User
    template_name = 'delete_user.html'
    success_url = reverse_lazy('index')


class LoginUserView(LoginView):
    """Login view."""

    template_name = 'login_user.html'
    success_url = reverse_lazy('index')
    redirect_authenticated_user = True


class LogoutUserView(LogoutView):
    """Logout view."""

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'GET':
            return HttpResponseForbidden('Unexpected method.') # TODO: make error page
        else:
            return super().dispatch(request, *args, **kwargs)


class UserView(DetailView):
    """User view."""

    template_name = 'user.html'
    model = User
