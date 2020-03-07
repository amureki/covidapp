from django.core.management.base import BaseCommand
from django.core.cache import cache

from data.models import Summary
from data.parser import parse_summary_data, parse_per_country_data


class Command(BaseCommand):
    help = "Parse COVID-19 data."

    def handle(self, *args, **options):
        self.stdout.write("Starting COVID-19 data parse...")

        raw_summary = parse_summary_data()
        raw_countries_data = parse_per_country_data()
        summary = Summary.objects.create(**raw_summary, raw_data=raw_countries_data)
        self.stdout.write("Parsed data: ")
        print(summary.get_summary_data())
        self.stdout.write("Clearing cache...")
        cache.clear()
        self.stdout.write("Done")
