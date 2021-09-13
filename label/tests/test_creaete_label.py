"""Tests."""

from django.test import TestCase, Client
from django.urls import reverse_lazy

from task_manager.tests.utils import (create_user,
                                      login_user,
                                      get_form_errors,
                                      get_last_message)

from label.models import Label


class CreateLabel(TestCase):
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
            'success': 'Метка успешно создана',
        }
        self.fields_errors = {
            'name_required': 'name:Обязательное поле.',
            'name_not_unique': 'name:Label с таким Имя уже существует.',
        }

    def test_create_valid_label(self):
        label = {'name': 'label name'}
        response = self.client.post(reverse_lazy('create_label'),
                                    data=label,
                                    follow=True)
        created_label_from_db = Label.objects.last()
        self.assertEqual(created_label_from_db.name,
                         label.get('name', None))
        self.assertEqual(Label.objects.count(), 1)
        self.assertEqual(get_last_message(response),
                         self.messages['success'])

    def test_create_not_unique_label(self):
        label = {'name': 'Label name'}
        for _ in range(2):
            response = self.client.post(reverse_lazy('create_label'),
                                        data=label,
                                        follow=True)
        self.assertEqual(Label.objects.count(), 1)
        self.assertIn(self.fields_errors['name_not_unique'],
                      get_form_errors(response))

    def test_create_label_if_data_not_full(self):
        label = {'name': ''}
        response = self.client.post(reverse_lazy('create_label'),
                                    data=label,
                                    follow=True)
        self.assertEqual(Label.objects.count(), 0)
        self.assertIn(self.fields_errors['name_required'],
                      get_form_errors(response))
