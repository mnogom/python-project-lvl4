"""Forms."""

from django.forms import ModelForm

from .models import Status


class StatusForm(ModelForm):
    """Status form.

    TODO: Edit translation 'имя' to 'название'
      in 'status:create' page.
    """

    class Meta:
        """Meta class."""

        model = Status
        fields = ('name',
                  'description',)
