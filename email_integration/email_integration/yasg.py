from django.urls import path
from django.conf import settings

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

if settings.DEBUG:
    schema_view = get_schema_view(
        openapi.Info(
            title="Django social",
            default_version='v1',
            description="Test description",
            license=openapi.License(name="BSD License"),
        ),
        public=True,
        permission_classes=[permissions.AllowAny]
    )

    urlpatterns = [
        path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    ]
else:
    urlpatterns = []
