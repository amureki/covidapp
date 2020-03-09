from rest_framework import serializers

from data.models import Summary


class SummarySerializer(serializers.ModelSerializer):
    countries_data = serializers.SerializerMethodField()

    class Meta:
        model = Summary
        fields = ["created", "confirmed", "deaths", "recovered", "countries_data"]

    def get_countries_data(self, obj):
        return obj.regions_data
