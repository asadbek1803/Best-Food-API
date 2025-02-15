from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .bot_views import (
    UserViewSet, CategoryViewSet, ProductViewSet, OrderViewSet, CartViewSet, DeliveryViewSet, 
    DriverLocationAPIView, RouteAPIView
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'products', ProductViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'cart', CartViewSet)
router.register(r'delivery', DeliveryViewSet)

urlpatterns = [
    path('<str:token>/', include(router.urls)),
    path('driver/location/<int:delivery_id>/', DriverLocationAPIView.as_view(), name='driver-location'),
    path('route/', RouteAPIView.as_view(), name='route'),
]
