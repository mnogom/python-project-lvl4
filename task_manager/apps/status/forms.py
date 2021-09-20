"""Forms."""

from django.forms import ModelForm

from .models import Status


class StatusForm(ModelForm):
    """Status form.

    TODO: Edit translation 'имя' to 'название'
      in 'create_status' page.
    """

    class Meta:
        """Meta class."""

        model = Status
        fields = ('name',
                  'description',)
