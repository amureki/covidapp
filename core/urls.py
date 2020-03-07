from django.contrib import admin
from django.urls import include, path

from api.v0.urls import router as v0_router

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v0/", include(v0_router.urls), name="v0"),
    path("", include("data.urls")),
]
