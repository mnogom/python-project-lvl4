"""Tests."""

from django.test import TestCase, Client
from django.urls import reverse_lazy
from django.forms.models import model_to_dict

from .views import ListStatusView
from .models import Status

from user.tests import create_user_and_login


class StatusAuthCase(TestCase):
    fixtures = ['status/fixtures/statuses.yaml', ]

    def setUp(self):
        self.client = Client()

    def test_unauth_access(self):
        response = self.client.get(reverse_lazy('statuses'))
        self.assertGreater(response.status_code, 200)

    def test_auth_access(self):
        create_user_and_login(self)
        response = self.client.get(reverse_lazy('statuses'))
        self.assertQuerysetEqual(
            response.context['object_list'].order_by('pk'),
            Status.objects.all().order_by('pk')
        )
        self.assertEqual(
            response.resolver_match.func.__name__,
            ListStatusView.as_view().__name__
        )


class StatusCreateCase(TestCase):
    def setUp(self):
        self.client = Client()
        create_user_and_login(self)

        status_name = 'status name'
        status_description = 'status description'

        self.valid_full_data = {'name': status_name,
                                'description': status_description}
        self.valid_part_data = {'name': status_name}
        self.not_valid_data = {'description': status_description}
        self.success_message = 'Статус успешно создан'

    def test_create_full_data_status(self):
        response = self.client.post(
            reverse_lazy('create_status'),
            follow=True,
            data=self.valid_full_data
        )

        self.assertEqual(
            response.context['messages']._loaded_data[-1].message,
            self.success_message
        )
        self.assertDictEqual(model_to_dict(Status.objects.last(),
                                           exclude='id'),
                             self.valid_full_data)
        self.assertEqual(response.redirect_chain[-1][0],
                         reverse_lazy('statuses'))

    def test_create_part_data_status(self):
        response = self.client.post(
            reverse_lazy('create_status'),
            follow=True,
            data=self.valid_part_data
        )

        self.assertEqual(
            response.context['messages']._loaded_data[-1].message,
            self.success_message
        )
        self.assertFalse(Status.objects.last().description)
        self.assertDictEqual(model_to_dict(Status.objects.last(),
                                           exclude=['id',
                                                    'description']),
                             self.valid_part_data)

    def test_create_not_valid_status(self):
        self.client.post(
            reverse_lazy('create_status'),
            follow=True,
            data=self.not_valid_data
        )
        self.assertEqual(
            len(Status.objects.all()),
            0
        )

    def test_create_not_unique_status(self):
        for _ in range(2):
            self.client.post(
                reverse_lazy('create_status'),
                follow=True,
                data=self.valid_full_data
            )
        response = self.client.get(reverse_lazy('statuses'))
        self.assertEqual(
            len(Status.objects.all()),
            1
        )


class StatusDeleteCase(TestCase):
    def setUp(self):
        self.client = Client()
        create_user_and_login(self)
        self.client.post(
            reverse_lazy('create_status'),
            data={'name': 'status name',
                  'description': 'status description'}
        )
        self.success_message = 'Статус успешно удалён'

    def test_delete_status(self):
        self.assertEqual(
            len(Status.objects.all()),
            1
        )
        response = self.client.post(
            reverse_lazy('delete_status', kwargs={'pk': 1}),
            follow=True
        )
        self.assertEqual(
            len(Status.objects.all()),
            0
        )
        self.assertEqual(
            response.context['messages']._loaded_data[-1].message,
            self.success_message
        )


class StatusEditCase(TestCase):
    def setUp(self):
        self.name_1 = 'status name 1'
        self.name_2 = 'status name 2'
        self.updated_name = 'updated name'

        self.client = Client()
        create_user_and_login(self)

        for name in [self.name_1, self.name_2]:
            self.client.post(
                reverse_lazy('create_status'),
                data={'name': name}
            )

    def test_valid_edit_status(self):
        self.assertEqual(
            len(Status.objects.all()),
            2
        )
        self.client.post(
            reverse_lazy('update_status', kwargs={'pk': 1}),
            data={'name': self.updated_name}
        )
        self.assertEqual(Status.objects.get(pk=1).name,
                         self.updated_name)

    def test_not_valid_edit_status(self):
        self.assertEqual(
            len(Status.objects.all()),
            2
        )
        self.client.post(
            reverse_lazy('update_status', kwargs={'pk': 1}),
            data={'name': self.name_2}
        )
        self.assertNotEqual(Status.objects.get(pk=1).name,
                            self.name_2)
