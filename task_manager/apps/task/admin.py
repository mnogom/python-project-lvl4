"""Admin panel."""

from django.contrib import admin
from .models import Task


class TaskAdmin(admin.ModelAdmin):
    """Admin panel for label."""
    pass


admin.site.register(Task, TaskAdmin)
