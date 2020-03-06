from django.urls import path

from data.views import IndexPageView

urlpatterns = [
    path("", IndexPageView.as_view(), name="index"),
]
