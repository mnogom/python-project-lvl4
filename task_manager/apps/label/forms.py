"""Forms."""

from django.forms import ModelForm

from .models import Label


class LabelForm(ModelForm):
    """Label form.
    """

    class Meta:
        """Meta class."""

        model = Label
        fields = ('name',)
