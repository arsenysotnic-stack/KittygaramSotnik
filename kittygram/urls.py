from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken import views
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from .views import index

schema_view = get_schema_view(
    openapi.Info(
        title="Kittygram API",
        default_version='v1',
        description="API для управления котиками и паспортами здоровья",
    ),
    public=True,
    patterns=[
        path('api/', include('cats.urls')),
        path('api/health/', include('health.urls')),
    ],
)

urlpatterns = [
    path('', index, name='index'),
    path('admin/', admin.site.urls),
    path('api/', include('cats.urls')),
    path('api/health/', include('health.urls')),
    path('api/auth/', include('djoser.urls')),
    path('api/auth/token/', views.obtain_auth_token, name='api_token_auth'),
    path('api/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
