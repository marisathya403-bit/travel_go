from django.contrib import admin
from .models import Destination


@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
        "state",
        "best_time",
        "average_budget",
        "created_at",
    )

    search_fields = (
        "name",
        "state",
    )

    list_filter = (
        "state",
        "best_time",
    )