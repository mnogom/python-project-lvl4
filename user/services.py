"""Services."""

from django.contrib.auth import authenticate, login, logout

from .forms import CreateUserForm
from .exceptions import UserFormIsNotValid
from .selectors import get_user_by_pk


def create_user(user_data):
    """Create user.

    :param user_data: data of user
    :return: created User
    """

    form = CreateUserForm(data=user_data)
    if form.is_valid():
        return form.save() # TODO: Password hash!
    raise UserFormIsNotValid


def login_user(request):
    """Login user."""

    user_data = request.POST.dict()
    user = authenticate(request, **user_data)
    if user is not None:
        login(request, user)
    else:
        raise Exception


def logout_user(request):
    """Logout user."""

    logout(request)


def delete_user(request, pk):
    """Delete user."""

    logout_user(request)
    user = get_user_by_pk(pk)
    user.delete()
