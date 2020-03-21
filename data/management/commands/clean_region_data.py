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
        regions = []
        for summary in Summary.objects.all():
            to_update = False
            raw_orig = summary.raw_data
            for item in raw_orig:
                region = item["attributes"]["Country_Region"]
                if region not in regions:
                    regions.append(region)

                if region == "Mainland China":
                    item["attributes"]["Country_Region"] = "China"
                    to_update = True
                if region == "Iran (Islamic Republic of)":
                    item["attributes"]["Country_Region"] = "Iran"
                    to_update = True
                if region in ("South Korea", "Republic of Korea", '"Korea; South"'):
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
                if region == "Republic of Moldova":
                    item["attributes"]["Country_Region"] = "Moldova"
                    to_update = True
                if region in ("Taiwan", "Taipei and environs"):
                    item["attributes"]["Country_Region"] = "Taiwan*"
                    to_update = True
                if region == "Russian Federation":
                    item["attributes"]["Country_Region"] = "Russia"
                    to_update = True
                if region == "Viet Nam":
                    item["attributes"]["Country_Region"] = "Vietnam"
                    to_update = True
                if region == "Vatican City":
                    item["attributes"]["Country_Region"] = "Holy See"
                    to_update = True
                if region in ("Gambia", "The Gambia"):
                    item["attributes"]["Country_Region"] = "Gambia, The"
                    to_update = True

            if to_update:
                summary.raw_data = raw_orig
                regions_data = summary.set_regions_data()
                Summary.objects.filter(pk=summary.pk).update(regions_data=regions_data)
        print(sorted(list(filter(None, regions))))
