"""Admin panel."""

from django.contrib import admin
from .models import Label


class LabelAdmin(admin.ModelAdmin):
    """Admin panel for label."""
    pass


admin.site.register(Label, LabelAdmin)
