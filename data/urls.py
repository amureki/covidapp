from django.urls import path

from data.views import IndexPageView, CountriesListView

urlpatterns = [
    path("", IndexPageView.as_view(), name="index"),
    path("countries/", CountriesListView.as_view(), name="countries"),
]
