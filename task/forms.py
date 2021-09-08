"""Forms."""

from django.forms import ModelForm

from .models import Task
from .exceptions import TaskAuthorIsMissing


class TaskForm(ModelForm):  # TODO: Make translation for fields
    """Model form."""

    class Meta:
        """Meta class."""

        model = Task
        fields = ('name',
                  'description',
                  'status',
                  'executor',
                  'labels',)

    def set_author(self, author_pk):
        self.instance.author_id = author_pk

    def save(self, **kwargs):
        """Save task method."""

        if getattr(self.instance, 'author', None) is None:
            raise TaskAuthorIsMissing("Author is missing. Use 'set_author()' method before save.")
        return super().save(**kwargs)
