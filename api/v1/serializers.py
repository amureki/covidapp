import pytz
from rest_framework import serializers

from data.models import Summary


class RegionListSerializer(serializers.Serializer):
    region = serializers.CharField(max_length=200)
    region_slug = serializers.CharField(max_length=200)

    class Meta:
        ref_name = "RegionListV1"


class RegionSerializer(serializers.Serializer):
    region = serializers.CharField(max_length=200)
    region_slug = serializers.CharField(max_length=200)
    lat = serializers.FloatField()
    long = serializers.FloatField()
    confirmed = serializers.IntegerField()
    deaths = serializers.IntegerField()
    recovered = serializers.IntegerField()
    updated = serializers.DateTimeField(default_timezone=pytz.utc)

    class Meta:
        ref_name = "RegionV1"


class WorldSerializer(serializers.ModelSerializer):
    regions_data = RegionSerializer(source="get_regions_data", many=True)
    created = serializers.SerializerMethodField()

    class Meta:
        model = Summary
        ref_name = "WorldV1"
        fields = ["created", "confirmed", "deaths", "recovered", "regions_data"]

    def get_created(self, obj):
        dt = obj.created.replace(microsecond=0).replace(tzinfo=None).isoformat()
        return dt + "Z"
