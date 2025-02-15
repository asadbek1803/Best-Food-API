from django.urls import path, include

urlpatterns = [
    path('bot/', include('bot_urls')),
    path('admin/', include('admin_urls'))
]
