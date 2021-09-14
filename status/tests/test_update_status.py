"""Tests update status."""

from django.test import TestCase, Client
from django.urls import reverse_lazy

from task_manager.tests.utils import (create_user,
                                      login_user,
                                      get_form_errors,
                                      get_last_message)

from status.models import Status


class UpdateStatus(TestCase):
    """Update status case."""

    def setUp(self) -> None:
        """Set up method."""

        self.client = Client()
        user = {'username': 'User',
                'password': 'Pass'}
        create_user(client=self.client,
                    user=user,
                    follow=False)
        login_user(client=self.client,
                   **user,
                   follow=False)

        self.status = [{'name': 'Name #1'},
                       {'name': 'Name #2'}, ]
        self.updated_status = {'name': 'New name (#3)'}
        for status in self.status:
            self.client.post(reverse_lazy('create_status'),
                             data=status,
                             follow=False)

        self.messages = {
            'success': 'Статус успешно изменён'
        }
        self.fields_errors = {
            'name_required': 'name:Обязательное поле.',
            'name_not_unique': 'name:Status с таким Имя уже существует.',
        }

    def test_update_status(self) -> None:
        """Test update status."""

        response = self.client.post(reverse_lazy('update_status',
                                                 kwargs={'pk': 1}),
                                    data=self.updated_status,
                                    follow=True)
        self.assertEqual(get_last_message(response),
                         self.messages['success'])
        self.assertEqual(Status.objects.get(pk=1).name,
                         self.updated_status.get('name', None))

    def test_update_status_to_not_unique(self) -> None:
        """Test update status with not unique fields."""

        response = self.client.post(reverse_lazy('update_status',
                                                 kwargs={'pk': 1}),
                                    data=self.status[1],
                                    follow=True)
        self.assertIn(self.fields_errors['name_not_unique'],
                      get_form_errors(response))
        self.assertEqual(Status.objects.get(pk=1).name,
                         self.status[0].get('name', None))

    def test_update_status_if_data_not_full(self) -> None:
        """Test update status without required fields."""

        response = self.client.post(reverse_lazy('update_status',
                                                 kwargs={'pk': 1}),
                                    follow=True)
        self.assertIn(self.fields_errors['name_required'],
                      get_form_errors(response))
