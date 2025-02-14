from django.urls import path
from .consumers import DriverLocationConsumer

websocket_urlpatterns = [
    path("ws/track/<int:order_id>/", DriverLocationConsumer.as_asgi()),
]
