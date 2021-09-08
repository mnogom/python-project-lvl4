from django.db import models

from django.db import models


class Label(models.Model):
    name = models.CharField(max_length=50,
                            unique=True,
                            blank=False,
                            null=False)
    created_at = models.DateField(auto_now_add=True,
                                  editable=False)

    def __str__(self):
        return self.name
