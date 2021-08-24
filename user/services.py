from django.contrib.auth.models import User

from .forms import UserForm


def create_user(user_data):
    form = UserForm(data=user_data)
    if form.is_valid():
        return form.save() # TODO: Password hash!
    raise Exception(f'{form.errors}')
