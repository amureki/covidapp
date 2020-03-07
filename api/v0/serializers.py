from rest_framework import serializers

from data.models import Summary


class SummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Summary
        fields = ["created", "confirmed", "deaths", "recovered"]
