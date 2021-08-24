"""Services."""

from .forms import CreateUserForm


def create_user(user_data):
    """Create user.

    :param user_data: data of user
    :return: created User
    """

    form = CreateUserForm(data=user_data)
    if form.is_valid():
        return form.save() # TODO: Password hash!
    raise Exception(f'{form.errors}')
