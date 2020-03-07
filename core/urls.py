from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from api.v0.urls import router as v0_router

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v0/", include(v0_router.urls), name="v0"),
    path("", include("data.urls")),
]

# swagger (by drf-yasg)
schema_view = get_schema_view(
    openapi.Info(
        title="Covidapp API",
        default_version="v0",
        contact=openapi.Contact(email="hi@amureki.me"),
        license=openapi.License(name="Apache License 2.0"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns += [
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
]
