from django.core.management.base import BaseCommand

from data.models import Summary
from data.parser import parse_data


class Command(BaseCommand):
    help = "Parse COVID-19 data."

    def handle(self, *args, **options):
        summary = parse_data()
        obj = Summary.create_from_data(summary)
        print(obj.get_summary_data())
