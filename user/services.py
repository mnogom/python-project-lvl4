"""Services."""

from django.contrib.auth import authenticate, login, logout

from .forms import EditUserForm
from .selectors import get_user_by_pk


def create_user(user_data):
    """Create user.

    :param user_data: data of user
    :return: created Form
    """

    form = EditUserForm(data=user_data)
    if form.is_valid():
        user = form.save()
        return user
    return None


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


def delete_user(pk):
    """Delete user."""

    user = get_user_by_pk(pk)
    user.delete()


def update_user(new_user_data, pk):
    user = get_user_by_pk(pk)
    form = EditUserForm(instance=user,
                        data=new_user_data)

    if form.is_valid():
        form.save()
    return form
