"""Models."""

from django.db import models
from django.utils.translation import gettext_lazy as _


class Status(models.Model):
    """Status model."""

    name = models.CharField(verbose_name=_('name'),
                            max_length=300,
                            unique=True,
                            blank=False,
                            null=False)
    description = models.TextField(verbose_name=_('description'),
                                   blank=True,
                                   null=False)
    created_at = models.DateField(verbose_name=_('created_at'),
                                  auto_now_add=True,
                                  editable=False)

    def __str__(self):
        """representation method."""

        return self.name
