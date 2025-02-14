from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, CategoryViewSet, ProductViewSet, OrderViewSet,
    CartViewSet, DeliveryViewSet, RatingViewSet, RouteAPIView, OrderStatusAPIView, DriverLocationAPIView, SalesStatisticsAPIView
)

router = DefaultRouter()
router.register(r'users/(?P<token>\d+)', UserViewSet, basename='user')
router.register(r'categories/(?P<token>\d+)', CategoryViewSet, basename='category')
router.register(r'products/(?P<token>\d+)', ProductViewSet, basename='product')
router.register(r'cart/(?P<token>\d+)', CartViewSet, basename='cart')
router.register(r'delivery/(?P<token>\d+)', DeliveryViewSet, basename='delivery')
router.register(r'ratings/(?P<token>\d+)', RatingViewSet, basename='rating')
router.register(r'orders/(?P<token>\d+)', OrderViewSet, basename='order')

# router.register(r'route/(?P<token>\d+)', RouteViewSet, basename="route")

urlpatterns = [
    path('', include(router.urls)), 
    path('route/calculate/', RouteAPIView.as_view()), #ishlad,
    path('statistics/', SalesStatisticsAPIView.as_view(), name='statistics'),
    path('order/status/<int:order_id>/', OrderStatusAPIView.as_view(), name='order-status'),
    path('driver/location/<int:delivery_id>/', DriverLocationAPIView.as_view(), name='driver-location'),

      # APIView uchun alohida qo‘shildi
]
