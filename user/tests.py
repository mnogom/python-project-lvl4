"""Tests."""

from django.test import TestCase, tag
from django.forms.models import model_to_dict
import yaml

from .models import User
from .exceptions import UserDoesNotExist
from .selectors import (get_all_users,
                        get_user_by_pk)
from .services import (create_user,
                       delete_user,
                       update_user,
                       login_user,
                       logout_user)


class UserSelectorsCase(TestCase):
    fixtures = ['user/fixtures/users.yaml']

    def setUp(self):
        self.pk = 1

        with open(self.fixtures[0], 'rb') as file:
            self.expected_users = yaml.safe_load(file)
        for user in self.expected_users:
            if user['pk'] == self.pk:
                self.expected_user = user['fields']
                self.expected_user.pop('password')
                break

    @tag('solo-selector')
    def test_solo_selector(self):
        user = get_user_by_pk(self.pk)

        # Check if data is similar after picking
        self.assertEqual(model_to_dict(user, fields=('username',
                                                     'first_name',
                                                     'last_name',
                                                     'email')),
                         self.expected_user)

        # Check if raises error after picking wrong pk
        with self.assertRaises(UserDoesNotExist):
            get_user_by_pk(-1)

    @tag('query-selector')
    def test_query_selector(self):
        users = get_all_users()
        self.assertEqual(len(users),
                         len(self.expected_users))


class UserServicesCase(TestCase):
    fixtures = ['user/fixtures/users.yaml']

    @tag('create-service')
    def test_create(self):
        # Check if service can create Status
        valid_data = {'username': 'test_username',
                      'first_name': 'test_first_name',
                      'last_name': 'test_last_name',
                      'email': 'test.address@domain.com',
                      'password1': 'qwerty',
                      'password2': 'qwerty',
                      'junk_key': 'junk_value'}
        form = create_user(valid_data)
        self.assertTrue(form.is_valid())

        # Check if all fields created right
        pk = form.instance.pk
        new_user = get_user_by_pk(pk)
        self.assertEqual(getattr(new_user, 'username'),
                         valid_data['username'])
        self.assertEqual(getattr(new_user, 'first_name'),
                         valid_data['first_name'])
        self.assertEqual(getattr(new_user, 'last_name'),
                         valid_data['last_name'])
        self.assertEqual(getattr(new_user, 'email'),
                         valid_data['email'])
        self.assertIsNone(getattr(new_user, 'junk_value', None))

        # Check if created password is secured
        self.assertNotEqual(getattr(new_user, 'password'),
                            valid_data['password1'])

        # Check if skip required data
        wrong_data = {'username': 'Simon',
                      'first_name': 'Simon',
                      'password1': '123',
                      'password2': '123'}
        form = create_user(wrong_data)
        self.assertFalse(form.is_valid())

        # Check if 'name' is not unique
        unique_data = {'username': 'unique',
                       'first_name': '?unique?',
                       'last_name': '?unique?',
                       'email': 'un@iq.ue',
                       'password1': '?unique?',
                       'password2': '?unique?'}
        form_1 = create_user(unique_data)
        form_2 = create_user(unique_data)
        self.assertTrue(form_1.is_valid())
        self.assertFalse(form_2.is_valid())

        # Check if password doesn't match
        unique_data = {'username': 'password_does_not_match',
                       'first_name': 'password_does_not_match',
                       'last_name': 'password_does_not_match',
                       'email': 'password_does@not.match',
                       'password1': 'password_does_not_match',
                       'password2': 'password??'}
        form = create_user(unique_data)
        self.assertFalse(form.is_valid())

    @tag('edit-service')
    def test_edit(self):
        # Check if service can edit Status
        new_user_data = {'username': 'test_username',
                         'first_name': 'test_first_name',
                         'last_name': 'test_last_name',
                         'email': 'test.address@domain.com',
                         'password1': 'qwerty',
                         'password2': 'qwerty'}
        _new_user_data = new_user_data.copy()
        _new_user_data.pop('password1')
        _new_user_data.pop('password2')

        user = get_user_by_pk(1)
        form = update_user(new_user_data, pk=1)
        updated_user = get_user_by_pk(1)
        self.assertTrue(form.is_valid())
        self.assertNotEqual(model_to_dict(user),
                            model_to_dict(updated_user))
        self.assertEqual(
            model_to_dict(updated_user, fields=('username',
                                                'first_name',
                                                'last_name',
                                                'email')),
            _new_user_data)

        # Check if created password is secured
        self.assertNotEqual(getattr(updated_user, 'password'),
                            new_user_data['password1'])

        # Check editing Status has unique protect
        unique_data_1 = {'username': 'unique_1',
                         'first_name': '?unique_1?',
                         'last_name': '?unique_1?',
                         'email': 'un_1@iq.ue',
                         'password1': '?unique_1?',
                         'password2': '?unique_1?'}
        unique_data_2 = {'username': 'unique_2',
                         'first_name': '?unique_2?',
                         'last_name': '?unique_2?',
                         'email': 'un_2@iq.ue',
                         'password1': '?unique_2?',
                         'password2': '?unique_2?'}
        not_unique_data = unique_data_1
        form_1 = create_user(unique_data_1)
        form_2 = create_user(unique_data_2)
        form_2_updated = update_user(not_unique_data, pk=form_2.instance.pk)
        self.assertTrue(form_1.is_valid())
        self.assertTrue(form_2.is_valid())
        self.assertFalse(form_2_updated.is_valid())

    @tag('delete-services')
    def test_delete(self):
        user_data = {'username': 'test_username',
                     'first_name': 'test_first_name',
                     'last_name': 'test_last_name',
                     'email': 'test.address@domain.com',
                     'password1': 'qwerty',
                     'password2': 'qwerty'}
        user_to_del = create_user(user_data)
        before_delete_len = len(get_all_users())
        delete_user(user_to_del.instance.pk)
        after_delete_len = len(get_all_users())
        self.assertNotEqual(before_delete_len,
                            after_delete_len)

    @tag('login_user')
    def test_login(self):
        pass

    @tag('logout_user')
    def test_logout(self):
        pass
