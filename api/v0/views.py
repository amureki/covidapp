from rest_framework import viewsets

from api.v0.serializers import SummarySerializer
from data.models import Summary


class SummaryViewSet(viewsets.ModelViewSet):
    queryset = Summary.objects.all()
    serializer_class = SummarySerializer
