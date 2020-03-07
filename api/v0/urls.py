from rest_framework import routers

from api.v0.views import SummaryViewSet

router = routers.DefaultRouter()
router.register(r"summary", SummaryViewSet)
