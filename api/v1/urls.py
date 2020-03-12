from django.urls import path

from api.v1.views import (
    WorldAPIView,
    WorldByDateAPIView,
    RegionAPIView,
    RegionByDateAPIView,
    RegionsAPIView,
)

urlpatterns = [
    path("world/", WorldAPIView.as_view(), name="world"),
    path(
        "world/<int:year>-<int:month>-<int:day>/",
        WorldByDateAPIView.as_view(),
        name="world-by-date",
    ),
    path("regions/", RegionsAPIView.as_view(), name="regions"),
    path("region/<str:region>/", RegionAPIView.as_view(), name="region"),
    path(
        "region/<str:region>/<int:year>-<int:month>-<int:day>/",
        RegionByDateAPIView.as_view(),
        name="region-by-date",
    ),
]
