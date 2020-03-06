from django.core.management.base import BaseCommand

from data.parser import parse_data


class Command(BaseCommand):
    help = "Parse COVID-19 data."

    def handle(self, *args, **options):
        stats = parse_data()
        print(stats)
