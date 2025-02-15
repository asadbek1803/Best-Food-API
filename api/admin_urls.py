from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .admin_views import (
    OrderViewSet, ProductViewSet, DeliveryViewSet, RatingViewSet,
    SalesStatisticsAPIView, AdminLoginAPIView, AdminLogoutAPIView, AdminProfileAPIView, UserViewSet
)

router = DefaultRouter()
router.register(r'orders', OrderViewSet)
router.register(r'products', ProductViewSet)
router.register(r'delivery', DeliveryViewSet)
router.register(r'ratings', RatingViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('statistics/', SalesStatisticsAPIView.as_view(), name='sales-statistics'),
    path("login/", AdminLoginAPIView.as_view(), name="admin-login"),
    path("logout/", AdminLogoutAPIView.as_view(), name="admin-logout"),
    path("profile/", AdminProfileAPIView.as_view(), name="admin-profile"),
]
