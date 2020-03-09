from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.text import slugify
from django_extensions.db.models import TimeStampedModel


class Summary(TimeStampedModel):
    confirmed = models.PositiveIntegerField()
    deaths = models.PositiveIntegerField()
    recovered = models.PositiveIntegerField()
    raw_data = JSONField()
    regions_data = JSONField(default=list)

    class Meta:
        verbose_name_plural = "Summaries"
        ordering = ["-created"]

    def __str__(self):
        return f"Summary from {self.created}"

    def save(self, **kwargs):
        self.regions_data = [
            {
                "region": region["attributes"]["Country_Region"],
                "region_slug": slugify(region["attributes"]["Country_Region"]),
                "confirmed": region["attributes"]["Confirmed"],
                "deaths": region["attributes"]["Deaths"],
                "recovered": region["attributes"]["Recovered"],
                "lat": region["attributes"]["Lat"],
                "long": region["attributes"]["Long_"],
                "updated": int(str(region["attributes"]["Last_Update"])[:-3]),
            }
            for region in self.raw_data
        ]
        super().save(**kwargs)

    def get_summary_data(self):
        return {
            "confirmed": self.confirmed,
            "deaths": self.deaths,
            "recovered": self.recovered,
        }
