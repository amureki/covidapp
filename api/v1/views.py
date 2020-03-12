from datetime import datetime

from django.http import Http404
from django.utils.text import slugify
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response

from api.v1.serializers import WorldSerializer, RegionSerializer, RegionListSerializer
from data.models import Summary, Region


class WorldAPIView(RetrieveAPIView):
    serializer_class = WorldSerializer

    def get_object(self):
        summary = Summary.objects.first()
        if not summary:
            raise Http404
        return summary


class WorldByDateAPIView(RetrieveAPIView):
    serializer_class = WorldSerializer

    def get_object(self):
        kwargs = self.kwargs
        try:
            dt = datetime(
                year=kwargs.get("year"),
                month=kwargs.get("month"),
                day=kwargs.get("day"),
                hour=23,
                minute=59,
            )
        except ValueError:
            raise Http404

        summary = Summary.objects.filter(created__lte=dt).first()
        if not summary:
            raise Http404

        return summary


class RegionsAPIView(WorldAPIView):
    queryset = Summary.objects.none()
    serializer_class = RegionListSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        regions = [item["region"] for item in instance.regions_data]
        data = [{"region": c, "region_slug": slugify(c)} for c in regions]
        serializer = self.get_serializer(data, many=True)
        return Response(serializer.data)


class RegionRetrieveMixin:
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        region_slug = self.kwargs.get("region").lower()
        region_data = next(
            (
                item
                for item in instance.regions_data
                if item["region_slug"] == region_slug
            ),
            None,
        )
        if not region_data:
            raise Http404

        serializer = self.get_serializer(Region(region_data))
        return Response(serializer.data)


class RegionAPIView(RegionRetrieveMixin, WorldAPIView):
    serializer_class = RegionSerializer


class RegionByDateAPIView(RegionRetrieveMixin, WorldByDateAPIView):
    serializer_class = RegionSerializer
