"""Tests create user."""

from django.test import TestCase, Client

from task_manager.tests.utils import (create_user,
                                      get_form_errors,
                                      get_last_message)

from task_manager.apps.user.models import User


class CreateUser(TestCase):
    """User create case."""

    def setUp(self) -> None:
        """Set up method."""

        self.client = Client()
        self.messages = {
            'success': 'Пользователь успешно зарегистрирован',
        }
        self.fields_errors = {
            'username_not_unique': 'username:Пользователь с таким именем уже существует.',
            'username_required': 'username:Обязательное поле.',
            'password1_required': 'password1:Обязательное поле.',
            'password_doesnt_math': 'password2:Введенные пароли не совпадают.',
        }

    def test_create_valid_user(self) -> None:
        """Test create user with valid fields."""

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
            created_user_from_db = User.objects.last()
            self.assertEqual(
                [
                    user.get('username', ''),
                    user.get('first_name', ''),
                    user.get('last_name', ''),
                    user.get('email', ''),
                ],
                [
                    created_user_from_db.username,
                    created_user_from_db.first_name,
                    created_user_from_db.last_name,
                    created_user_from_db.email,
                ])

            # Check if password is secure
            self.assertNotEqual(user['password'],
                                created_user_from_db.password)
            self.assertEqual(get_last_message(response=response),
                             self.messages['success'])
        self.assertEqual(User.objects.count(), 2)

    def test_create_not_unique_user(self) -> None:
        """Test create user with not unique fields."""

        user = {'username': 'Username',
                'password': 'Password'}
        for _ in range(2):
            response = create_user(client=self.client,
                                   user=user,
                                   follow=True)
        self.assertEqual(User.objects.count(), 1)
        self.assertIn(self.fields_errors['username_not_unique'],
                      get_form_errors(response))

    def test_create_if_user_data_not_full(self) -> None:
        """Test create user without required fields."""

        user = {'first_name': 'First',
                'password': 'password'}
        response = create_user(client=self.client,
                               user=user,
                               follow=True)
        self.assertEqual(User.objects.count(), 0)
        self.assertIn(self.fields_errors['username_required'],
                      get_form_errors(response))

        user = {'username': 'Username',
                'first_name': 'First',
                'password2': 'Password'}
        response = create_user(client=self.client,
                               user=user,
                               follow=True)
        self.assertEqual(User.objects.count(), 0)
        self.assertIn(self.fields_errors['password1_required'],
                      get_form_errors(response))

    def test_create_if_passwords_doesnt_match(self) -> None:
        """Test create user if passwords doesn't match."""

        user = {'username': 'Username',
                'password1': 'password1',
                'password2': 'password2'}
        response = create_user(client=self.client,
                               user=user,
                               follow=True)
        self.assertEqual(User.objects.count(), 0)
        self.assertIn(self.fields_errors['password_doesnt_math'],
                      get_form_errors(response))
