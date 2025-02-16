from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.admin_views import (
    OrderViewSet, ProductViewSet, DeliveryViewSet, RatingViewSet, OrderItemsViewSet,
    SalesStatisticsAPIView, AdminLoginAPIView, AdminLogoutAPIView,
    AdminProfileAPIView, UserViewSet, AdminTokenRefreshView
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
     # Login (Access & Refresh token oladi)
    path("login/", AdminLoginAPIView.as_view(), name="admin-login"),
    
    # Logout (Tokenni o‘chirish)
    path("logout/", AdminLogoutAPIView.as_view(), name="admin-logout"),

    # Access token olish (Refresh token orqali yangilash)
    path("token/refresh/", AdminTokenRefreshView.as_view(), name="token-refresh"),
    path("profile/", AdminProfileAPIView.as_view(), name="admin-profile"),
]
