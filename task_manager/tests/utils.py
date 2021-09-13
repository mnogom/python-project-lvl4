from django.urls import reverse_lazy
from django.contrib.messages import get_messages


def _post_from_user(user):
    post_data = {
        'username': user.get('username', ''),
        'email': user.get('email', ''),
        'first_name': user.get('first_name', ''),
        'last_name': user.get('last_name', ''),
    }
    if 'password' in user.keys():
        post_data['password1'] = user.get('password')
        post_data['password2'] = user.get('password')
    else:
        post_data['password1'] = user.get('password1', ''),
        post_data['password2'] = user.get('password2', '')
    return post_data


def create_user(client, user=None, follow=False):
    if not user:
        user = {'username': 'Username',
                'email': 'username@email.com',
                'password': 'password'}
    return client.post(
        reverse_lazy('create_user'),
        data=_post_from_user(user),
        follow=follow
    )


def login_user(client, username, password, follow=False):
    return client.post(
        reverse_lazy('login'),
        data={'username': username,
              'password': password},
        follow=follow
    )


def get_last_message(response):
    # return response.context['messages'].loaded_data[-1].message
    try:
        return str(get_messages(response.wsgi_request)._loaded_data[-1])
    except IndexError:
        return ''


def get_form_errors(response):
    errors = []
    try:
        form_errors = response.context_data['form']._errors.as_data()
    except AttributeError:
        return errors

    if form_errors:
        for key, values in form_errors.items():
            for value in values:
                # TODO: [fix] ¯\_(ツ)_/¯
                errors.append(
                    '{}:{}'.format(key, *value)
                )
    return errors
