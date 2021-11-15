"""Forms."""

from django.forms import ModelForm

from .models import Label


class LabelForm(ModelForm):
    """Label form.

    TODO: Edit translation 'имя' to 'название'
      in 'label:create' page.
    """

    class Meta:
        """Meta class."""

        model = Label
        fields = ('name',)
