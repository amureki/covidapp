from django.contrib.postgres.fields import JSONField
from django.db import models
from django_extensions.db.models import TimeStampedModel


class Summary(TimeStampedModel):
    confirmed = models.IntegerField()
    deaths = models.IntegerField()
    recovered = models.IntegerField()
    raw_data = JSONField()
    countries_data = JSONField(default=list)

    class Meta:
        verbose_name_plural = "Summaries"
        ordering = ["-created"]

    def __str__(self):
        return f"Summary from {self.created}"

    def save(self, **kwargs):
        self.countries_data = [
            {
                "region": country["attributes"]["Country_Region"],
                "confirmed": country["attributes"]["Confirmed"],
                "deaths": country["attributes"]["Deaths"],
                "recovered": country["attributes"]["Recovered"],
                "lat": country["attributes"]["Lat"],
                "long": country["attributes"]["Long_"],
                "updated": int(str(country["attributes"]["Last_Update"])[:-3]),
            }
            for country in self.raw_data
        ]
        super().save(**kwargs)

    def get_summary_data(self):
        return {
            "confirmed": self.confirmed,
            "deaths": self.deaths,
            "recovered": self.recovered,
        }
