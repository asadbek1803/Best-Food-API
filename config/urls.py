"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.urls import re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .settings import DEBUG, STATIC_ROOT, STATIC_URL, MEDIA_URL, MEDIA_ROOT



schema_view = get_schema_view(
   openapi.Info(
      title="Best Food API",
      default_version='v1',
      description="Best Food API Mini APP uchun yaratilgan maxsus API hisoblanadi BUG bo'lsa iltimos men bilan bog'laning.",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="asadbekoffical1202@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.IsAdminUser,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/bot/', include("api.urls"), name="apis"),
    path('api/v2/admin/', include("accounts.urls")),
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]


if DEBUG:
    urlpatterns += static(STATIC_URL, document_root=STATIC_ROOT)
    urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)