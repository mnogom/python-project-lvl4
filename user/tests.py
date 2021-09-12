"""Tests."""

from django.test import TestCase, Client
from django.urls import reverse_lazy
from django.forms.models import model_to_dict
from django.contrib.messages import get_messages

from .views import ListUsersView
from .models import User


def _post_from_user(user):
    return {
        'username': user.get('username', ''),
        'email': user.get('email', ''),
        'first_name': user.get('first_name', ''),
        'last_name': user.get('last_name', ''),
        'password1': user.get('password', ''),
        'password2': user.get('password', '')
    }


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
    return str(get_messages(response.wsgi_request)._loaded_data[-1])


def get_form_errors(response):
    form_errors = response.context_data['form']._errors.as_data()
    errors = []
    if form_errors:
        for key, values in form_errors.items():
            for value in values:
                # TODO: [fix] ¯\_(ツ)_/¯
                errors.append(
                    '{}:{}'.format(key, *value)
                )
    return errors


class CreateUser(TestCase):
    def setUp(self):
        self.client = Client()

        self.messages = {
            'success': 'Пользователь успешно зарегистрирован',
            'errors': {
                'username_not_unique': 'Пользователь с таким именем уже существует.'
            }
        }

    def test_create_valid_user(self):
        user_full = {'username': 'Username-1',
                     'first_name': 'First-1',
                     'last_name': 'Last-1',
                     'email': 'username-1@email.com',
                     'password': 'Password-1'}
        user_part = {'username': 'Username-2',
                     'password': 'Password-2'}

        for user in [user_full, user_part]:
            response = create_user(client=self.client,
                                   user=user,
                                   follow=True)
            created_user = User.objects.last()
            self.assertEqual(
                [
                    user.get('username', ''),
                    user.get('first_name', ''),
                    user.get('last_name', ''),
                    user.get('email', ''),
                ],
                [
                    created_user.username,
                    created_user.first_name,
                    created_user.last_name,
                    created_user.email,
                ])
            self.assertNotEqual(user['password'],
                                created_user.password)
            self.assertEqual(get_last_message(response=response),
                             self.messages['success'])
        self.assertEqual(User.objects.count(), 2)

    def test_create_not_unique_user(self):
        user = {'username': 'Username',
                'password': 'Password'}
        for _ in range(2):
            response = create_user(client=self.client,
                                   user=user,
                                   follow=True)
        # get_form_errors(response)
        # self.assertIn(self.not_unique_username_message,
        #               get_form_errors(response))
        self.assertEqual(User.objects.count(), 1)


# def create_user_and_login(obj, userdata=None):
#     """Function to create and login user."""
#     if not userdata:
#         userdata = {'username': 'Username',
#                     'email': 'username@email.com',
#                     'password1': 'password',
#                     'password2': 'password'}
#     obj.client.post(
#         reverse_lazy('create_user'),
#         data=userdata
#     )
#     obj.client.post(
#         reverse_lazy('login'),
#         data={'username': userdata['username'],
#               'password': userdata['password1']}
#     )
#
#
# class UserAuthCase(TestCase):
#     """User authentication case."""
#
#     fixtures = ['user/fixtures/users.yaml', ]
#
#     def setUp(self):
#         self.client = Client()
#
#     def test_unauth_access(self):
#         response = self.client.get(reverse_lazy('users'))
#         self.assertQuerysetEqual(
#             response.context['object_list'].order_by('pk'),
#             User.objects.all().order_by('pk')
#         )
#
#     def test_auth_access(self):
#         create_user_and_login(self)
#         response = self.client.get(reverse_lazy('users'))
#         self.assertQuerysetEqual(
#             response.context['object_list'].order_by('pk'),
#             User.objects.all().order_by('pk')
#         )
#
#
# class UserCreateCase(TestCase):
#     def setUp(self):
#         self.client = Client()
#         username = 'Username'
#         email = 'Email@mail.com'
#         password = 'Password'
#         first_name = 'First'
#         last_name = 'Last'
#
#         self.valid_full_data = {'username': username,
#                                 'email': email,
#                                 'password1': password,
#                                 'password2': password,
#                                 'first_name': first_name,
#                                 'last_name': last_name}
#         self.valid_part_data = {'username': username,
#                                 'password1': password,
#                                 'password2': password}
#         self.not_valid_data = [
#             {'email': email,
#              'password1': password,
#              'password2': password},
#             {'username': username,
#              'password1': password + '1',
#              'password2': password + '2'}
#         ]
#         self.success_message = 'Пользователь успешно зарегистрирован'
#
#     def test_create_full_data_user(self):
#         response = self.client.post(
#             reverse_lazy('create_user'),
#             follow=True,
#             data=self.valid_full_data
#         )
#
#         self.assertEqual(
#             response.context['messages']._loaded_data[-1].message,
#             self.success_message
#         )
#
#         self.assertEqual(
#             [User.objects.last().username,
#              User.objects.last().first_name,
#              User.objects.last().last_name],
#             [self.valid_full_data.get('username', ''),
#              self.valid_full_data.get('first_name', ''),
#              self.valid_full_data.get('last_name', '')]
#         )
#
#         self.assertNotEqual(
#             User.objects.last().password,
#             self.valid_full_data.get('password1', '')
#         )
#
#     def test_create_part_data_user(self):
#         response = self.client.post(
#             reverse_lazy('create_user'),
#             follow=True,
#             data=self.valid_part_data
#         )
#
#         self.assertEqual(
#             response.context['messages']._loaded_data[-1].message,
#             self.success_message
#         )
#
#         self.assertEqual(
#             [User.objects.last().username,
#              User.objects.last().first_name,
#              User.objects.last().last_name],
#             [self.valid_part_data.get('username', ''),
#              self.valid_part_data.get('first_name', ''),
#              self.valid_part_data.get('last_name', '')]
#         )
#
#         self.assertNotEqual(
#             User.objects.last().password,
#             self.valid_part_data.get('password1', '')
#         )
#
#     def test_create_not_valid_user(self):
#         for data in self.not_valid_data:
#             self.client.post(
#                 reverse_lazy('create_user'),
#                 follow=True,
#                 data=data
#             )
#
#             self.assertEqual(
#                 len(User.objects.all()),
#                 0
#             )
#
#     def test_create_not_unique_user(self):
#         for _ in range(2):
#             self.client.post(
#                 reverse_lazy('create_user'),
#                 follow=True,
#                 data=self.valid_part_data
#             )
#
#             self.assertEqual(
#                 len(User.objects.all()),
#                 1
#             )
#
#
# class UserLogCase(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.username = 'Username'
#         self.password = 'Password'
#         self.userdata = {'username': self.username,
#                          'password1': self.password,
#                          'password2': self.password}
#         self.client.post(
#             reverse_lazy('create_user'),
#             data=self.userdata
#         )
#
#         self.success_login_message = 'Вы залогинены'
#         self.success_logout_message = 'Вы разлогинены'
#
#     def test_success_login_logout_user(self):
#         response = self.client.post(
#             reverse_lazy('login'),
#             data={'username': self.username,
#                   'password': self.password},
#             follow=True
#         )
#
#         self.assertEqual(response.redirect_chain[-1][0],
#                          reverse_lazy('index'))
#         self.assertEqual(
#             response.context['messages']._loaded_data[-1].message,
#             self.success_login_message
#         )
#
#         response = self.client.post(
#             reverse_lazy('logout'),
#             follow=True
#         )
#
#         self.assertEqual(response.redirect_chain[-1][0],
#                          reverse_lazy('index'))
#         self.assertEqual(
#             response.context['messages']._loaded_data[-1].message,
#             self.success_logout_message
#         )
#
#     def test_unsuccess_login_user(self):
#         response = self.client.post(
#             reverse_lazy('login'),
#             data={'username': self.username,
#                   'password': self.password + '_'},
#             follow=True
#         )
#         self.assertFalse(response.context_data['form'].is_valid())
#
#
# class UserDeleteCase(TestCase):
#     def setUp(self):
#         self.client = Client()
#         create_user_and_login(self)
#         self.success_message = 'Пользователь успешно удалён'
#
#     def test_delete(self):
#         self.assertEqual(len(User.objects.all()),
#                          1)
#         self.client.post(reverse_lazy('delete_user', kwargs={'pk': 1}))
#         self.assertEqual(len(User.objects.all()),
#                          0)
#
#
# class UserEditCase(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.userdata_1 = {'username': 'Username-1',
#                            'password': 'Password-1'}
#         self.userdata_2 = {'username': 'Username-2',
#                            'password': 'Password-2'}
#         self.new_valid_username = 'Username-100-500'
#         self.success_message = 'Пользователь успешно изменён'
#
#         for user in [self.userdata_1, self.userdata_2]:
#             self.client.post(
#                 reverse_lazy('create_user'),
#                 data={'username': user['username'],
#                       'password1': user['password'],
#                       'password2': user['password']},
#                 follow=True
#             )
#         self.client.post(
#             reverse_lazy('login'),
#             data=self.userdata_1
#         )
#
#     def test_success_edit(self):
#         response = self.client.post(
#             reverse_lazy('update_user', kwargs={'pk': 1}),
#             data={'username': self.new_valid_username,
#                   'password1': self.userdata_1['password'],
#                   'password2': self.userdata_1['password']},
#             follow=True
#         )
#
#         self.assertNotEqual(User.objects.get(pk=1).username,
#                             self.userdata_1['username'])
#         self.assertEqual(User.objects.get(pk=1).username,
#                          self.new_valid_username)
#         self.assertEqual(response.context['messages']._loaded_data[-1].message,
#                          self.success_message)
#         self.denied_message = ''
#
#     def test_unsuccess_edit(self):
#         response = self.client.post(
#             reverse_lazy('update_user', kwargs={'pk': 1}),
#             data={'username': self.userdata_2['username'],
#                   'password1': self.userdata_1['password'],
#                   'password2': self.userdata_1['password']},
#             follow=True
#         )
#         self.assertFalse(response.context_data['form'].is_valid())
#         self.assertNotEqual(User.objects.get(pk=1).username,
#                             self.userdata_2['username'])
#         self.assertEqual(User.objects.get(pk=1).username,
#                          self.userdata_1['username'])
#
#     def test_edit_another_user(self):
#         response = self.client.post(
#             reverse_lazy('update_user', kwargs={'pk': 2}),
#             data={'username': self.new_valid_username,
#                   'password1': self.userdata_2['password'],
#                   'password2': self.userdata_2['password']},
#             follow=True
#         )
#         self.assertNotEqual(
#             User.objects.get(pk=2).username,
#             self.new_valid_username
#         )
