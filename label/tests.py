"""Tests."""

from django.test import TestCase, Client
from django.urls import reverse_lazy
from django.forms.models import model_to_dict

from .views import ListLabelView
from .models import Label

from user.tests import create_user_and_login


class LabelAuthCase(TestCase):
    fixtures = ['label/fixtures/labels.yaml', ]

    def setUp(self):
        self.client = Client()

    def test_unauth_access(self):
        response = self.client.get(reverse_lazy('labels'))
        self.assertGreater(response.status_code, 200)

    def test_auth_access(self):
        create_user_and_login(self)
        response = self.client.get(reverse_lazy('labels'))
        self.assertQuerysetEqual(
            response.context['object_list'].order_by('pk'),
            Label.objects.all().order_by('pk')
        )
        self.assertEqual(
            response.resolver_match.func.__name__,
            ListLabelView.as_view().__name__
        )


class LabelCreateCase(TestCase):
    def setUp(self):
        self.client = Client()
        create_user_and_login(self)

        self.valid_full_data = {'name': 'label name'}
        self.not_valid_data = {'name': ''}
        self.success_message = 'Метка успешно создана'

    def test_create_full_data_label(self):
        response = self.client.post(
            reverse_lazy('create_label'),
            follow=True,
            data=self.valid_full_data
        )

        self.assertEqual(
            response.context['messages']._loaded_data[-1].message,
            self.success_message
        )
        self.assertDictEqual(model_to_dict(Label.objects.last(),
                                           exclude='id'),
                             self.valid_full_data)
        self.assertEqual(response.redirect_chain[-1][0],
                         reverse_lazy('labels'))

    def test_create_not_valid_label(self):
        self.client.post(
            reverse_lazy('create_label'),
            follow=True,
            data=self.not_valid_data
        )
        self.assertEqual(
            len(Label.objects.all()),
            0
        )

    def test_create_not_unique_label(self):
        for _ in range(2):
            self.client.post(
                reverse_lazy('create_label'),
                follow=True,
                data=self.valid_full_data
            )
        response = self.client.get(reverse_lazy('labels'))
        self.assertEqual(
            len(Label.objects.all()),
            1
        )


class LabelDeleteCase(TestCase):
    def setUp(self):
        self.client = Client()
        create_user_and_login(self)
        self.client.post(
            reverse_lazy('create_label'),
            data={'name': 'label name',
                  'description': 'label description'}
        )
        self.success_message = 'Метка успешно удалена'

    def test_delete_label(self):
        self.assertEqual(
            len(Label.objects.all()),
            1
        )
        response = self.client.post(
            reverse_lazy('delete_label', kwargs={'pk': 1}),
            follow=True
        )
        self.assertEqual(
            len(Label.objects.all()),
            0
        )
        self.assertEqual(
            response.context['messages']._loaded_data[-1].message,
            self.success_message
        )


class LabelEditCase(TestCase):
    def setUp(self):
        self.name_1 = 'label name 1'
        self.name_2 = 'label name 2'
        self.updated_name = 'updated name'

        self.client = Client()
        create_user_and_login(self)

        for name in [self.name_1, self.name_2]:
            self.client.post(
                reverse_lazy('create_label'),
                data={'name': name}
            )

    def test_valid_edit_label(self):
        self.assertEqual(
            len(Label.objects.all()),
            2
        )
        self.client.post(
            reverse_lazy('update_label', kwargs={'pk': 1}),
            data={'name': self.updated_name}
        )
        self.assertEqual(Label.objects.get(pk=1).name,
                         self.updated_name)

    def test_not_valid_edit_label(self):
        self.assertEqual(
            len(Label.objects.all()),
            2
        )
        self.client.post(
            reverse_lazy('update_label', kwargs={'pk': 1}),
            data={'name': self.name_2}
        )
        self.assertNotEqual(Label.objects.get(pk=1).name,
                            self.name_2)
