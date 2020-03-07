from django.contrib import admin

from data.models import Summary


class SummaryAdmin(admin.ModelAdmin):
    list_display = ("id", "confirmed", "deaths", "recovered", "created")
    list_display_links = ("id", "created")


admin.site.register(Summary, SummaryAdmin)
