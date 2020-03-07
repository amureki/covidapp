from django.contrib.postgres.fields import JSONField
from django.db import models
from django_extensions.db.models import TimeStampedModel


class Summary(TimeStampedModel):
    confirmed = models.IntegerField()
    deaths = models.IntegerField()
    recovered = models.IntegerField()
    original_data = JSONField()

    class Meta:
        verbose_name_plural = "Summaries"
        ordering = ["-created"]

    def __str__(self):
        return f"Summary from {self.created}"

    def get_summary_data(self):
        return {
            "confirmed": self.confirmed,
            "deaths": self.deaths,
            "recovered": self.recovered,
        }

    @classmethod
    def create_from_data(cls, data):
        data["original_data"] = data.copy()
        return Summary.objects.create(**data)
