"""Models."""

from django.db import models
from django.utils.translation import gettext_lazy as _


class Label(models.Model):
    name = models.CharField(verbose_name=_('name'),
                            max_length=50,
                            unique=True,
                            blank=False,
                            null=False)
    created_at = models.DateField(verbose_name=_('created at'),
                                  auto_now_add=True,
                                  editable=False)

    def __str__(self):
        return self.name
