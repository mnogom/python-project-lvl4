"""Forms."""

from django.forms import ModelForm

from .models import Task
from .exceptions import TaskAuthorIsMissing


class TaskForm(ModelForm):
    """Model form.

    TODO: [fix] Edit translation 'имя' to 'название'
     in 'task:create' page.
    """

    class Meta:
        """Meta class."""

        model = Task
        fields = ('name',
                  'description',
                  'status',
                  'executor',
                  'labels',)

    def set_author(self, author_pk: int):
        """Set author for task method.

        :param author_pk: author pk (id)
        """

        self.instance.author_id = author_pk

    def save(self, **kwargs):
        """Save task method."""

        if getattr(self.instance, 'author', None) is None:
            raise TaskAuthorIsMissing("Author is missing. Use 'set_author()' method before save.")
        return super().save(**kwargs)
