"""Tests."""

from django.test import TestCase, tag
from django.forms.models import model_to_dict
import yaml

from .models import Status
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

    @tag('create-service')
    def test_create(self):

        # Check if service can create Status
        valid_data = {'name': 'test_name',
                      'description': 'test_description',
                      'junk_key': 'junk_value',
                      'created_at': '1990-01-01'}
        form = create_status(valid_data)
        self.assertTrue(form.is_valid())

        # Check if all fields created right
        pk = form.instance.pk
        new_status = get_status_by_pk(pk)
        self.assertEqual(getattr(new_status, 'name', None),
                         valid_data['name'])
        self.assertEqual(getattr(new_status, 'description', None),
                         valid_data['description'])
        self.assertEqual(getattr(new_status, 'junk_key', None),
                         None)
        self.assertNotEqual(getattr(new_status, 'created_at', None),
                            valid_data['created_at'])

        # Check if skip required data
        wrong_data = {'description': 'A'}
        form = create_status(wrong_data)
        self.assertFalse(form.is_valid())

        # Check if 'name' is not unique
        unique_data = {'name': '?unique?'}
        _ = create_status(unique_data)
        form = create_status(unique_data)
        self.assertFalse(form.is_valid())

    @tag('edit-service')
    def test_edit(self):

        # Check if service can edit Status
        new_status_data = {'name': 'updated_name',
                           'description': 'updated_description'}
        status = get_status_by_pk(1)
        form = update_status(new_status_data, pk=1)
        updated_status = get_status_by_pk(1)
        self.assertTrue(form.is_valid())
        self.assertNotEqual(model_to_dict(status),
                            model_to_dict(updated_status))
        self.assertEqual(model_to_dict(updated_status, exclude=('id', )),
                         new_status_data)

        # Check editing Status has unique protect
        unique_data = {'name': '?unique_edit?'}
        create_status(unique_data)
        form = update_status(unique_data, pk=1)
        self.assertFalse(form.is_valid())


    @tag('delete-service')
    def test_delete(self):
        status_to_del = create_status({'name': 'delete'})
        before_delete_len = len(get_all_statuses())
        delete_status(status_to_del.instance.pk)
        after_delete_len = len(get_all_statuses())
        self.assertNotEqual(before_delete_len,
                            after_delete_len)
