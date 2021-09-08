"""Forms."""

from django.forms import ModelForm

from .models import Status


class StatusForm(ModelForm):  # TODO: Make translation for fields
    """Status form"""

    class Meta:
        """Meta class."""

        model = Status
        fields = ('name',
                  'description',)
