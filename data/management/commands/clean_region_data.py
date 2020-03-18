from django.core.management.base import BaseCommand

from data.models import Summary

MISSING_FULL_DATASET = [
    "taiwan",
    "bulgaria",
    "brunei",
    "panama",
    "cyprus",
    "moldova",
    "maldives",
    "bolivia",
    "kazakhstan",
    "paraguay",
    "reunion",
    "turkey",
    "cuba",
    "uruguay",
    "ghana",
    "bangladesh",
    "jersey",
    "congo",
    "faso",
    "aruba",
    "Namibia",
    "Seychelles",
    "Honduras",
    "Venezuela",
    "Trinidad",
    "Holy See",
    "Cote d'Ivoire",
    "curacao",
    "suriname",
    "sudan",
    "Equatorial Guinea",
    "Guadeloupe",
    "Guyana",
    "Mauritania",
    "Guernsey",
    "Eswatini",
    "Antigua and Barbuda",
    "Guatemala",
    "Ethiopia",
    "Saint Vincent and the Grenadines",
    "Kenya",
    "Gabon",
    "Saint Lucia",
    "Mongolia",
    "Rwanda",
    "Cayman Islands",
    "Guinea",
]


class Command(BaseCommand):
    help = "Clean region naming data."

    def handle(self, *args, **options):
        for summary in Summary.objects.all():
            to_update = False
            raw_orig = summary.raw_data
            for item in raw_orig:
                region = item["attributes"]["Country_Region"]
                if region == "Mainland China":
                    item["attributes"]["Country_Region"] = "China"
                    to_update = True
                if region == "Iran (Islamic Republic of)":
                    item["attributes"]["Country_Region"] = "Iran"
                    to_update = True
                if region in ("South Korea", "Republic of Korea"):
                    item["attributes"]["Country_Region"] = "Korea, South"
                    to_update = True
                if region == "UK":
                    item["attributes"]["Country_Region"] = "United Kingdom"
                    to_update = True
                if region == "Others":
                    item["attributes"]["Country_Region"] = "Cruise Ship"
                    to_update = True
                if region == "Czech Republic":
                    item["attributes"]["Country_Region"] = "Czechia"
                    to_update = True
                if region == "Taiwan":
                    item["attributes"]["Country_Region"] = "Taiwan*"
                    to_update = True
                if region == "Russian Federation":
                    item["attributes"]["Country_Region"] = "Russia"
                    to_update = True
                if region == "Viet Nam":
                    item["attributes"]["Country_Region"] = "Vietnam"
                    to_update = True
            if to_update:
                summary.raw_data = raw_orig
                regions_data = summary.set_regions_data()
                Summary.objects.filter(pk=summary.pk).update(regions_data=regions_data)
