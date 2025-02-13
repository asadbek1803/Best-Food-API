from django.urls import re_path
from .consumers import DriverLocationConsumer

websocket_urlpatterns = [
    re_path(r"ws/location/(?P<order_id>\d+)/$", DriverLocationConsumer.as_asgi()),
]
