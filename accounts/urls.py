from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.admin_views import (
    OrderViewSet, ProductViewSet, DeliveryViewSet, RatingViewSet, OrderItemsViewSet,
    SalesStatisticsAPIView, AdminLoginAPIView, AdminLogoutAPIView, AdminProfileAPIView, UserViewSet
)

router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename="admin-orders")
router.register(r'products', ProductViewSet, basename="admin-products")
router.register(r'delivery', DeliveryViewSet, basename="admin-delivery")
router.register(r'ratings', RatingViewSet, basename="admin-ratings")
router.register(r'users', UserViewSet, basename="admin-users")
router.register(r'order/items', OrderItemsViewSet, basename="admin-order-itmes")

urlpatterns = [
    path('', include(router.urls)),
    path('statistics/', SalesStatisticsAPIView.as_view(), name='sales-statistics'),
    path("login/", AdminLoginAPIView.as_view(), name="admin-login"),
    path("logout/", AdminLogoutAPIView.as_view(), name="admin-logout"),
    path("profile/", AdminProfileAPIView.as_view(), name="admin-profile"),
]
