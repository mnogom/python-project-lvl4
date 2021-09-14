"""Tests."""

from django.test import TestCase, Client
from django.urls import reverse_lazy

from task_manager.tests.utils import (create_user,
                                      login_user,
                                      get_last_message)
from user.models import User


def _reverse_lazy_with_filter(url_name, **kwargs):
    url = f'{reverse_lazy(url_name)}?'
    for key, value in kwargs.items():
        url += f'{key}={value}'
    return url


class Filter(TestCase):
    fixtures = ['user/fixtures/users.yaml',
                'status/fixtures/statuses.yaml',
                'label/fixtures/labels.yaml',
                'task/fixtures/tasks.yaml']

    def setUp(self):
        self.client = Client()
        self.user = User.objects.get(pk=1)
        self.client.force_login(self.user)

    def test_filter_by_author(self):
        url = _reverse_lazy_with_filter('users', author=1)
        response = self.client.get(url)
