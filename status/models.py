from django.db import models


class Status(models.Model):
    name = models.CharField(max_length=300,
                            unique=True,
                            blank=False,
                            null=False)
    description = models.TextField(blank=True,
                                   null=False)
    created_at = models.DateField(auto_now_add=True, editable=False)
