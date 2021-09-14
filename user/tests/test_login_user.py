"""Tests login user."""

from django.test import TestCase, Client
from django.urls import reverse_lazy

from task_manager.tests.utils import (create_user,
                                      login_user,
                                      get_form_errors,
                                      get_last_message)


class LoginUser(TestCase):
    """Login user case."""

    def setUp(self) -> None:
        """Set up method."""

        self.client = Client()
        self.user = {'username': 'username',
                     'password': 'Password'}

        self.messages = {
            'success_login': 'Вы залогинены',
            'success_logout': 'Вы разлогинены',
        }
        self.fields_errors = {
            'invalid_data': '__all__:Пожалуйста, введите правильные '
                            'имя пользователя и пароль. Оба поля могут '
                            'быть чувствительны к регистру.',
        }

    def test_valid_login(self) -> None:
        """Test login with valid information."""

        create_user(self.client,
                    user=self.user,
                    follow=False)
        response = login_user(self.client,
                              **self.user,
                              follow=True)
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertEqual(self.messages['success_login'],
                         get_last_message(response))

    def test_invalid_login(self) -> None:
        """Test login with not valid information."""

        response = login_user(self.client,
                              **self.user,
                              follow=True)
        self.assertFalse(response.context['user'].is_authenticated)
        self.assertIn(self.fields_errors['invalid_data'],
                      get_form_errors(response))

    def test_logout(self) -> None:
        """Test logout."""

        create_user(self.client,
                    user=self.user,
                    follow=False)
        login_user(self.client,
                   **self.user,
                   follow=True)
        response = self.client.post(reverse_lazy('logout'),
                                    follow=True)
        self.assertFalse(response.context['user'].is_authenticated)
        self.assertEqual(get_last_message(response),
                         self.messages['success_logout'])
