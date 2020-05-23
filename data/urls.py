from django.urls import path
from django.views.generic import TemplateView

from data.views import IndexPageView, RegionsListView, RegionDetailView

urlpatterns = [
    path("", IndexPageView.as_view(), name="index"),
    path("regions/", RegionsListView.as_view(), name="regions"),
    path("region/<slug:region>/", RegionDetailView.as_view(), name="region"),
    path(
        "support/", TemplateView.as_view(template_name="support.html"), name="support"
    ),
]
