from rest_framework import routers

from api.v0.views import CountrySummaryViewSet, CountryViewSet, SummaryViewSet

router = routers.DefaultRouter()
router.register(r"countries", CountryViewSet, basename="countries")
router.register(r"summary/country", CountrySummaryViewSet, basename="country")
router.register(r"summary", SummaryViewSet, basename="summary")
