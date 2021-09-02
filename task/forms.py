"""Forms."""

from django.forms import ModelForm

from .models import Task
from .fields import (name_field,
                     description_field,
                     status_field,
                     executor_field)


class StatusForm(ModelForm):
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
