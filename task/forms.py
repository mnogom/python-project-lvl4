"""Forms."""

from django.forms import ModelForm

from user.selectors import get_user_by_pk

from .models import Task
from .fields import (name_field,
                     description_field,
                     status_field,
                     executor_field)
from .exceptions import TaskAuthorIsMissing


class TaskForm(ModelForm):
    """Model form."""

    name = name_field
    description = description_field
    status = status_field
    executor = executor_field

    class Meta:
        """Meta class."""

        model = Task
        fields = ('name',
                  'description',
                  'status',
                  'executor',)

    def set_author(self, author_pk):
        self.instance.author_id = author_pk

    def save(self, **kwargs):
        """Save task method."""

        if getattr(self.instance, 'author', None) is None:
            raise TaskAuthorIsMissing("Author is missing. Use 'set_author()' method before save.")
        return super().save(**kwargs)
