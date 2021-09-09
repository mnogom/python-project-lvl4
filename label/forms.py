"""Forms."""

from django.forms import ModelForm

from .models import Label


class LabelForm(ModelForm):
    """Status form"""
    # TODO: Edit translation 'имя' to 'название'
    #  in 'create_label' page.

    class Meta:
        """Meta class."""

        model = Label
        fields = ('name',)
