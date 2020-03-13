from django.contrib import admin

from data.models import Summary


class SummaryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "confirmed",
        "deaths",
        "recovered",
        "created",
        "is_latest_for_day",
    )
    list_display_links = ("id", "created")
    list_filter = ("is_latest_for_day",)


admin.site.register(Summary, SummaryAdmin)
