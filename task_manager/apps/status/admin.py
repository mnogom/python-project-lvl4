"""Admin panel."""

from django.contrib import admin
from .models import Status


class StatusAdmin(admin.ModelAdmin):
    pass


admin.site.register(Status, StatusAdmin)
