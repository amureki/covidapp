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
