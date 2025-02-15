from django.urls import path, include
import bot_urls
import admin_urls

urlpatterns = [
    path('bot/', include(bot_urls)),
    path('admin/', include(admin_urls))
]
