"""Services."""

from django.contrib.auth import authenticate, login, logout
from django.db.models import ProtectedError

from .forms import UserForm
from .selectors import get_user_by_pk


def create_user(user_data):
    """Create user.

    :param user_data: data of user
    :return: created Form
    """

    form = UserForm(data=user_data)
    if form.is_valid():
        form.save()
    return form


def delete_user(pk):
    """Delete user."""

    user = get_user_by_pk(pk)
    try:
        return user.delete()
    except ProtectedError:
        return None


def update_user(new_user_data, pk):
    user = get_user_by_pk(pk)
    form = UserForm(instance=user,
                    data=new_user_data)
    if form.is_valid():
        form.save()
    return form


def login_user(request):
    """Login user."""

    username = request.POST.get('username')
    password = request.POST.get('password1')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return True
    return False


def logout_user(request):
    """Logout user."""

    logout(request)
