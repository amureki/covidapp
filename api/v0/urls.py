from rest_framework import routers

from api.v0.views import CountrySummaryViewSet, CountryViewSet, SummaryViewSet

router = routers.DefaultRouter()
router.register(r"countries", CountryViewSet)
router.register(r"summary/country", CountrySummaryViewSet)
router.register(r"summary", SummaryViewSet)
