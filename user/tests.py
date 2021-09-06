# """Tests."""
#
# import yaml
#
# from django.test import TestCase, tag
# from django.forms.models import model_to_dict
# from django.shortcuts import resolve_url
#
# from task_manager import http_status
#
# from .exceptions import UserDoesNotExist
# from .selectors import (get_all_users,
#                         get_user_by_pk)
# from .services import (create_user,
#                        delete_user,
#                        update_user)
#
#
# class UserSelectorsCase(TestCase):
#     fixtures = ['user/fixtures/users.yaml']
#
#     def setUp(self):
#         self.pk = 1
#
#         with open(self.fixtures[0], 'rb') as file:
#             self.expected_users = yaml.safe_load(file)
#         for user in self.expected_users:
#             if user['pk'] == self.pk:
#                 self.expected_user = user['fields']
#                 self.expected_user.pop('password')
#                 break
#
#     @tag('solo-selector')
#     def test_solo_selector(self):
#         user = get_user_by_pk(self.pk)
#
#         # Check if data is similar after picking
#         self.assertEqual(model_to_dict(user, fields=('username',
#                                                      'first_name',
#                                                      'last_name',
#                                                      'email')),
#                          self.expected_user)
#
#         # Check if raises error after picking wrong pk
#         with self.assertRaises(UserDoesNotExist):
#             get_user_by_pk(-1)
#
#     @tag('query-selector')
#     def test_query_selector(self):
#         users = get_all_users()
#         self.assertEqual(len(users),
#                          len(self.expected_users))
#
#
# class UserServicesCase(TestCase):
#     fixtures = ['user/fixtures/users.yaml', ]
#
#     def setUp(self):
#         self.overfull_data = {'username': 'test_username',
#                               'first_name': 'test_first_name',
#                               'last_name': 'test_last_name',
#                               'email': 'test.address@domain.com',
#                               'password1': 'qwerty',
#                               'password2': 'qwerty',
#                               'junk_key': 'junk_value'}
#         self.not_full_data = {'username': 'Simon',
#                               'first_name': 'Simon',
#                               'password1': '123',
#                               'password2': '123'}
#         self.unique_data_1 = {'username': 'unique_1',
#                               'first_name': 'Unique first name 1',
#                               'last_name': 'Unique last name 1',
#                               'email': 'un_1@iq.ue',
#                               'password1': 'unique_1',
#                               'password2': 'unique_1'}
#         self.unique_data_2 = {'username': 'unique_2',
#                               'first_name': 'Unique first name 2',
#                               'last_name': 'Unique first name 2',
#                               'email': 'un_2@iq.ue',
#                               'password1': 'unique_2',
#                               'password2': 'unique_2'}
#
#     @tag('create-service')
#     def test_create(self):
#         """Check if service can create User."""
#
#         form = create_user(self.overfull_data)
#         self.assertTrue(form.is_valid())
#
#         # Check if all fields created right
#         new_user = form.instance
#         self.assertEqual(getattr(new_user, 'username'),
#                          self.overfull_data['username'])
#         self.assertEqual(getattr(new_user, 'first_name'),
#                          self.overfull_data['first_name'])
#         self.assertEqual(getattr(new_user, 'last_name'),
#                          self.overfull_data['last_name'])
#         self.assertEqual(getattr(new_user, 'email'),
#                          self.overfull_data['email'])
#         self.assertIsNone(getattr(new_user, 'junk_value', None))
#
#         # Check if created password is secured
#         self.assertNotEqual(getattr(new_user, 'password'),
#                             self.overfull_data['password1'])
#
#     @tag('create-service-exception')
#     def test_create_exception_not_full_data(self):
#         """Check if skip required data."""
#
#         form = create_user(self.not_full_data)
#         self.assertFalse(form.is_valid())
#
#     @tag('create-service-exception')
#     def test_create_exception_unique(self):
#         """Check if 'name' is not unique."""
#
#         form_1 = create_user(self.unique_data_1)
#         form_2 = create_user(self.unique_data_1)
#         self.assertTrue(form_1.is_valid())
#         self.assertFalse(form_2.is_valid())
#
#     @tag('create-service-exception')
#     def test_create_exception_passwords(self):
#         """Check if password doesn't match."""
#
#         user_data = self.unique_data_1
#         user_data['password2'] = user_data['password1'] + '_'
#         form = create_user(user_data)
#         self.assertFalse(form.is_valid())
#
#     @tag('edit-service')
#     def test_edit(self):
#         """Check if service can edit User."""
#
#         _unique_data = self.unique_data_2.copy()
#         _unique_data.pop('password1')
#         _unique_data.pop('password2')
#         form_1 = create_user(self.unique_data_1)
#         form_2 = update_user(self.unique_data_2, pk=form_1.instance.pk)
#         self.assertTrue(form_1.is_valid())
#         self.assertTrue(form_2.is_valid())
#         self.assertNotEqual(model_to_dict(form_1.instance),
#                             model_to_dict(form_2.instance))
#         self.assertEqual(model_to_dict(form_2.instance,
#                                        fields=('username',
#                                                'first_name',
#                                                'last_name',
#                                                'email',)),
#                          _unique_data)
#
#         # Check if updated password is secured
#         self.assertNotEqual(getattr(form_2.instance, 'password'),
#                             self.unique_data_2['password1'])
#
#     @tag('edit-service-exception')
#     def test_edit_exception_unique(self):
#         """Check editing User has unique protect."""
#
#         not_unique_data = self.unique_data_1
#         form = create_user(self.unique_data_1)
#         form_before_update = create_user(self.unique_data_2)
#         form_after_update = update_user(not_unique_data, pk=form_before_update.instance.pk)
#         self.assertTrue(form.is_valid())
#         self.assertTrue(form_before_update.is_valid())
#         self.assertFalse(form_after_update.is_valid())
#
#     @tag('delete-service')
#     def test_delete(self):
#         user_to_del = create_user(self.unique_data_1)
#         before_delete_len = len(get_all_users())
#         delete_user(user_to_del.instance.pk)
#         after_delete_len = len(get_all_users())
#         self.assertNotEqual(before_delete_len,
#                             after_delete_len)
#
#
# class UserAuthCase(TestCase):
#     login_url = resolve_url('login')
#
#     def setUp(self):
#         self.existing_user = {'username': 'User',
#                               'password1': 'qwerty'}
#         self.existing_user_with_wrong_password = self.existing_user
#         self.existing_user['password1'] += 'wrong_password'
#         self.not_existing_user = {'username': 'Not_existing_user',
#                                   'password1': 'qwerty'}
#
#         user_data = {'username': self.existing_user['username'],
#                      'first_name': 'test_first_name',
#                      'last_name': 'test_last_name',
#                      'email': 'test.address@domain.com',
#                      'password1': self.existing_user['password1'],
#                      'password2': self.existing_user['password1']}
#         create_user(user_data)
#
#     def test_login(self):
#         """Login."""
#
#         response = self.client.post(self.login_url,
#                                     data=self.existing_user)
#         self.assertTrue(response.status_code, http_status.HTTP_302_FOUND)
#
#         response = self.client.post(self.login_url,
#                                     data=self.existing_user_with_wrong_password)
#         self.assertTrue(response.status_code, http_status.HTTP_400_BAD_REQUEST)
#
#         response = self.client.post(self.login_url,
#                                     data=self.not_existing_user)
#         self.assertTrue(response.status_code, http_status.HTTP_400_BAD_REQUEST)
#
#
# class UserAccessCase(TestCase):
#
#     def setUp(self):
#         self.user = {'username': 'User',
#                      'password1': 'qwerty'}
#         user_data = {'username': self.user['username'],
#                      'first_name': 'test_first_name',
#                      'last_name': 'test_last_name',
#                      'email': 'test.address@domain.com',
#                      'password1': self.user['password1'],
#                      'password2': self.user['password1']}
#         form = create_user(user_data)
#
#         self.users_url = resolve_url('users')
#         self.create_user_url = resolve_url('create_user')
#         self.update_user_url = resolve_url('update_user', form.instance.pk)
#         self.delete_user_url = resolve_url('delete_user', form.instance.pk)
#         self.login_url = resolve_url('login')
#         self.logout_url = resolve_url('logout')
#
#     def test_unauth_user(self):
#         response = self.client.get(self.users_url)
#         self.assertTrue(response.status_code, http_status.HTTP_200_OK)
#
#         response = self.client.get(self.create_user_url)
#         self.assertTrue(response.status_code, http_status.HTTP_200_OK)
#
#         response = self.client.get(self.update_user_url)
#         self.assertTrue(response.status_code, http_status.HTTP_302_FOUND)
#         self.assertTrue(response.get('location', None),
#                         resolve_url('login'))
#
#         response = self.client.get(self.delete_user_url)
#         self.assertTrue(response.status_code, http_status.HTTP_302_FOUND)
#         self.assertTrue(response.get('location', None),
#                         resolve_url('login'))
#
#         response = self.client.get(self.login_url)
#         self.assertTrue(response.status_code, http_status.HTTP_200_OK)
#
#         response = self.client.get(self.logout_url)
#         self.assertTrue(response.status_code,
#                         http_status.HTTP_405_METHOD_NOT_ALLOWED)
#
#     def test_auth_user(self):
#         self.client.post(resolve_url(self.login_url), data=self.user)
#
#         response = self.client.get(self.users_url)
#         self.assertTrue(response.status_code, http_status.HTTP_200_OK)
#
#         response = self.client.get(self.create_user_url)
#         self.assertTrue(response.status_code, http_status.HTTP_302_FOUND)
#
#         response = self.client.get(self.update_user_url)
#         self.assertTrue(response.status_code, http_status.HTTP_200_OK)
#
#         response = self.client.get(self.delete_user_url)
#         self.assertTrue(response.status_code, http_status.HTTP_200_OK)
#
#         response = self.client.get(self.login_url)
#         self.assertTrue(response.status_code, http_status.HTTP_302_FOUND)
#
#         response = self.client.get(self.logout_url)
#         self.assertTrue(response.status_code,
#                         http_status.HTTP_405_METHOD_NOT_ALLOWED)
#
#
