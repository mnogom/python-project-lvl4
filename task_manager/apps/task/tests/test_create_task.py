"""Tests create task."""


from django.test import TestCase, Client
from django.urls import reverse_lazy

from task_manager.tests.utils import (get_last_message,
                                      get_form_errors)

from task_manager.apps.task.models import Task
from task_manager.apps.user.models import User


class CreateTask(TestCase):
    """"""

    fixtures = ['task_manager/fixtures/users.yaml',
                'task_manager/fixtures/statuses.yaml',
                'task_manager/fixtures/labels.yaml']

    def setUp(self) -> None:
        """Set up method."""

        self.author = User.objects.get(pk=1)
        self.executor_pk = 2
        self.status_pk = 3
        self.labels_pk = [1, 2, 3]

        self.client = Client()
        self.client.force_login(self.author)

        self.messages = {
            'success': 'Задача успешно создана'
        }
        self.fields_errors = {
            'name_not_unique': 'name:Задача с таким названием уже существует',
            'name_required': 'name:Обязательное поле.',
            'executor_required': 'executor:Обязательное поле.',
            'status_required': 'status:Обязательное поле.',
        }

    def test_create_valid_task(self) -> None:
        """Test create task with valid fields."""

        task_full = {'name': 'Task #1',
                     'description': 'Some description',
                     'executor': self.executor_pk,
                     'status': self.status_pk,
                     'labels': self.labels_pk}
        task_part = {'name': 'Task #2',
                     'executor': self.executor_pk,
                     'status': self.status_pk}

        for task in [task_full, task_part]:
            response = self.client.post(reverse_lazy('create_task'),
                                        data=task,
                                        follow=True)
            self.assertEqual(get_last_message(response),
                             self.messages['success'])

            created_task_from_db = Task.objects.last()
            self.assertEqual(
                [
                    task.get('name', ''),
                    task.get('description', ''),
                    task.get('status', ''),
                    self.author.pk,
                    task.get('executor', ''),
                    task.get('labels', [])
                ],
                [
                    created_task_from_db.name,
                    created_task_from_db.description,
                    created_task_from_db.status.pk,
                    created_task_from_db.author.pk,
                    created_task_from_db.executor.pk,
                    list(
                        created_task_from_db.labels.values_list('pk', flat=True)
                    )
                ]
            )
        self.assertEqual(Task.objects.count(), 2)

    def test_create_not_unique_task(self) -> None:
        """Test create task with not unique fields."""

        task = {'name': 'Task #2',
                'executor': self.executor_pk,
                'status': self.status_pk}
        for _ in range(2):
            response = self.client.post(reverse_lazy('create_task'),
                                        data=task,
                                        follow=True)
        self.assertEqual(Task.objects.count(), 1)
        self.assertIn(self.fields_errors['name_not_unique'],
                      get_form_errors(response))

    def test_create_if_task_data_not_full(self) -> None:
        """Test create task without required fields."""

        task_without_name = {'executor': self.executor_pk,
                             'status': self.status_pk}
        response = self.client.post(reverse_lazy('create_task'),
                                    data=task_without_name,
                                    follow=True)
        self.assertEqual(Task.objects.count(), 0)
        self.assertIn(self.fields_errors['name_required'],
                      get_form_errors(response))

        task_without_executor = {'name': 'Task #2',
                                 'status': self.status_pk}
        response = self.client.post(reverse_lazy('create_task'),
                                    data=task_without_executor,
                                    follow=True)
        self.assertEqual(Task.objects.count(), 0)
        self.assertIn(self.fields_errors['executor_required'],
                      get_form_errors(response))

        task_without_status = {'name': 'Task #3',
                               'executor': self.executor_pk}
        response = self.client.post(reverse_lazy('create_task'),
                                    data=task_without_status,
                                    follow=True)
        self.assertEqual(Task.objects.count(), 0)
        self.assertIn(self.fields_errors['status_required'],
                      get_form_errors(response))
