from django.utils.text import slugify
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from api.v0.pagination import CustomPageNumberPagination
from api.v0.serializers import SummarySerializer
from data.models import Summary


class SummaryViewSet(ListModelMixin, GenericViewSet):
    queryset = Summary.objects.all()
    serializer_class = SummarySerializer
    pagination_class = CustomPageNumberPagination

    @action(detail=False)
    def latest(self, request):
        latest_summary = Summary.objects.first()

        serializer = self.get_serializer(latest_summary)
        return Response(serializer.data)


class CountryViewSet(GenericViewSet):
    queryset = Summary.objects.all()

    def list(self, request, *args, **kwargs):
        latest_summary = Summary.objects.first()
        countries = [item["region"] for item in latest_summary.countries_data]
        countries_data = {slugify(country): country for country in countries}
        return Response(countries_data)


class CountrySummaryViewSet(GenericViewSet):
    queryset = Summary.objects.all()
    serializer_class = None
    lookup_field = "slug"

    def retrieve(self, request, *args, **kwargs):
        latest_summary = Summary.objects.first()
        slug = self.kwargs.get("slug")
        country_data = next(
            (
                item
                for item in latest_summary.countries_data
                if item["region_slug"] == slug
            ),
            None,
        )
        country_data["created"] = latest_summary.created
        return Response(country_data)
