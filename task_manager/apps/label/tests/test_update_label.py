"""Tests update label."""

from django.test import TestCase, Client
from django.urls import reverse_lazy

from task_manager.tests.utils import (create_user,
                                      login_user,
                                      get_form_errors,
                                      get_last_message)

from task_manager.apps.label.models import Label


class UpdateLabel(TestCase):
    """Update label case."""

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

        self.labels = [{'name': 'Name #1'},
                       {'name': 'Name #2'}, ]
        self.updated_label = {'name': 'New name (#3)'}
        for label in self.labels:
            self.client.post(reverse_lazy('create_label'),
                             data=label,
                             follow=False)

        self.messages = {
            'success': 'Метка успешно изменена'
        }
        self.fields_errors = {
            'name_required': 'name:Обязательное поле.',
            'name_not_unique': 'name:Label с таким Имя уже существует.',
        }

    def test_update_label(self) -> None:
        """Test update label."""

        response = self.client.post(reverse_lazy('update_label',
                                                 kwargs={'pk': 1}),
                                    data=self.updated_label,
                                    follow=True)
        self.assertEqual(get_last_message(response),
                         self.messages['success'])
        self.assertEqual(Label.objects.get(pk=1).name,
                         self.updated_label.get('name', None))

    def test_update_label_to_not_unique(self) -> None:
        """Test update label with not unique fields."""

        response = self.client.post(reverse_lazy('update_label',
                                                 kwargs={'pk': 1}),
                                    data=self.labels[1],
                                    follow=True)
        self.assertIn(self.fields_errors['name_not_unique'],
                      get_form_errors(response))
        self.assertEqual(Label.objects.get(pk=1).name,
                         self.labels[0].get('name', None))

    def test_update_label_if_data_not_full(self) -> None:
        """Test update label without required fields."""

        response = self.client.post(reverse_lazy('update_label',
                                                 kwargs={'pk': 1}),
                                    follow=True)
        self.assertIn(self.fields_errors['name_required'],
                      get_form_errors(response))
