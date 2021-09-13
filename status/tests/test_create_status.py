"""Tests."""

from django.test import TestCase, Client
from django.urls import reverse_lazy

from task_manager.tests.utils import (create_user,
                                      login_user,
                                      get_form_errors,
                                      get_last_message)

from status.models import Status


class CreateStatus(TestCase):
    def setUp(self):
        self.client = Client()
        user = {'username': 'User',
                'password': 'Pass'}
        create_user(client=self.client,
                    user=user,
                    follow=False)
        login_user(client=self.client,
                   **user,
                   follow=False)

        self.messages = {
            'success': 'Статус успешно создан',
        }
        self.fields_errors = {
            'name_required': 'name:Обязательное поле.',
            'name_not_unique': 'name:Status с таким Имя уже существует.',
        }

    def test_create_valid_status(self):
        status = {'name': 'status name'}
        response = self.client.post(reverse_lazy('create_status'),
                                    data=status,
                                    follow=True)
        created_status_from_db = Status.objects.last()
        self.assertEqual(created_status_from_db.name,
                         status.get('name', None))
        self.assertEqual(Status.objects.count(), 1)
        self.assertEqual(get_last_message(response),
                         self.messages['success'])

    def test_create_not_unique_status(self):
        status = {'name': 'Status name'}
        for _ in range(2):
            response = self.client.post(reverse_lazy('create_status'),
                                        data=status,
                                        follow=True)
        self.assertEqual(Status.objects.count(), 1)
        self.assertIn(self.fields_errors['name_not_unique'],
                      get_form_errors(response))

    def test_create_status_if_data_not_full(self):
        status = {'name': ''}
        response = self.client.post(reverse_lazy('create_status'),
                                    data=status,
                                    follow=True)
        self.assertEqual(Status.objects.count(), 0)
        self.assertIn(self.fields_errors['name_required'],
                      get_form_errors(response))
