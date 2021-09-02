"""Tests."""

import yaml

from django.test import TestCase, tag
from django.forms.models import model_to_dict

from .exceptions import StatusDoesNotExist
from .selectors import (get_all_statuses,
                        get_status_by_pk)
from .services import (create_status,
                       delete_status,
                       update_status)


class StatusSelectorsCase(TestCase):
    fixtures = ['status/fixtures/statuses.yaml', ]

    def setUp(self):
        self.pk = 1

        with open(self.fixtures[0], 'rb') as file:
            self.expected_statuses = yaml.safe_load(file)
        for status in self.expected_statuses:
            if status['pk'] == self.pk:
                self.expected_status = status['fields']
                self.expected_status.pop('created_at')
                break

    @tag('solo-selector')
    def test_solo_selector(self):
        status = get_status_by_pk(self.pk)

        # Check if data is similar after picking
        self.assertEqual(model_to_dict(status, exclude=('id',)),
                         self.expected_status)

        # Check if raises error after picking wrong pk
        with self.assertRaises(StatusDoesNotExist):
            get_status_by_pk(-1)

    @tag('query-selector')
    def test_query_selector(self):
        statuses = get_all_statuses()
        self.assertEqual(len(statuses),
                         len(self.expected_statuses))


class StatusServicesCase(TestCase):
    fixtures = ['status/fixtures/statuses.yaml', ]

    def setUp(self):
        self.overfull_data = {'name': 'test_name',
                              'description': 'test_description',
                              'junk_key': 'junk_value',
                              'created_at': '1990-01-01'}
        self.not_full_data = {'description': 'A'}
        self.unique_data_1 = {'name': 'unique_name_1',
                              'description': 'unique_description_1'}
        self.unique_data_2 = {'name': 'unique_name_2',
                              'description': 'unique_description_2'}

    @tag('create-service')
    def test_create(self):
        """Check if service can create Status."""

        form = create_status(self.overfull_data)
        self.assertTrue(form.is_valid())

        # Check if all fields created right
        new_status = form.instance
        self.assertEqual(getattr(new_status, 'name'),
                         self.overfull_data['name'])
        self.assertEqual(getattr(new_status, 'description'),
                         self.overfull_data['description'])
        self.assertIsNone(getattr(new_status, 'junk_key', None))
        self.assertNotEqual(getattr(new_status, 'created_at'),
                            self.overfull_data['created_at'])

    @tag('create-service-exception')
    def test_create_exception_not_full_data(self):
        """Check if skip required data."""

        form = create_status(self.not_full_data)
        self.assertFalse(form.is_valid())

    @tag('create-service-exception')
    def test_create_exception_unique(self):
        """Check if 'name' is not unique."""

        form_1 = create_status(self.unique_data_1)
        form_2 = create_status(self.unique_data_1)
        self.assertTrue(form_1.is_valid())
        self.assertFalse(form_2.is_valid())

    @tag('edit-service')
    def test_edit(self):
        """Check if service can edit Status."""

        form_1 = create_status(self.unique_data_1)
        form_2 = update_status(self.unique_data_2, pk=form_1.instance.pk)
        self.assertTrue(form_1.is_valid())
        self.assertTrue(form_2.is_valid())
        self.assertNotEqual(model_to_dict(form_1.instance),
                            model_to_dict(form_2.instance))
        self.assertEqual(model_to_dict(form_2.instance,
                                       fields=('name',
                                               'description')),
                         self.unique_data_2)

    @tag('edit-service-exception')
    def test_edit_exception_unique(self):
        """Check editing Status has unique protect."""

        not_unique_data = self.unique_data_1
        form = create_status(self.unique_data_1)
        form_before_update = create_status(self.unique_data_2)
        form_after_update = update_status(not_unique_data, pk=form_before_update.instance.pk)
        self.assertTrue(form.is_valid())
        self.assertTrue(form_before_update.is_valid())
        self.assertFalse(form_after_update.is_valid())

    @tag('delete-service')
    def test_delete(self):
        status_to_del = create_status(self.unique_data_1)
        before_delete_len = len(get_all_statuses())
        delete_status(status_to_del.instance.pk)
        after_delete_len = len(get_all_statuses())
        self.assertNotEqual(before_delete_len,
                            after_delete_len)
