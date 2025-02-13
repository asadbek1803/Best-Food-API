from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, CategoryViewSet, ProductViewSet, CartViewSet, DeliveryViewSet, RatingViewSet, RouteView

router = DefaultRouter()
router.register(r'users/(?P<token>\d+)', UserViewSet, basename='user')
router.register(r'categories/(?P<token>\d+)', CategoryViewSet, basename='category')
router.register(r'products/(?P<token>\d+)', ProductViewSet, basename='product')
router.register(r'cart/(?P<token>\d+)', CartViewSet, basename='cart')
router.register(r'delivery/(?P<token>\d+)', DeliveryViewSet, basename='delivery')
router.register(r'ratings/(?P<token>\d+)', RatingViewSet, basename='rating')

urlpatterns = [
    path('', include(router.urls)),
    path(r'route/(?P<token>\d+)', RouteView.as_view(), name="route"),
]
