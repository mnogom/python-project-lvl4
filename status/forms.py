"""Fields."""

from django.forms import ModelForm

from .models import Status
from .fields import (name_field,
                     description_field)


class StatusForm(ModelForm):
    """Status form"""

    name = name_field
    description = description_field

    class Meta:
        """Meta class."""

        model = Status
        fields = ('name',
                  'description',)
