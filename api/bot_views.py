from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from .authentication import URLTokenAuthentication
from .models import User, Category, Product, Order, Cart, Delivery, Rating
from .serializers import UserSerializer, CategorySerializer, ProductSerializer, OrderSerializer, CartSerializer, DeliverySerializer, RatingSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from utils.graphhopper import get_route
from django.utils.timezone import now
from rest_framework.pagination import PageNumberPagination
import requests

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    lookup_field = "telegram_id"
    serializer_class = UserSerializer
    authentication_classes = [URLTokenAuthentication]
    pagination_class = StandardResultsSetPagination  
    permission_classes = [AllowAny]


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    lookup_field = "name"
    serializer_class = CategorySerializer
    pagination_class = StandardResultsSetPagination  
    authentication_classes = [URLTokenAuthentication]
    permission_classes = [AllowAny]


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.select_related('user', 'delivery').all()
    serializer_class = OrderSerializer
    authentication_classes = [URLTokenAuthentication]
    pagination_class = StandardResultsSetPagination  
    permission_classes = [AllowAny]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = StandardResultsSetPagination  
    authentication_classes = [URLTokenAuthentication]
    permission_classes = [AllowAny]


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.select_related('user', 'product').all()
    serializer_class = CartSerializer
    authentication_classes = [URLTokenAuthentication]
    pagination_class = StandardResultsSetPagination  
    permission_classes =[AllowAny]


class DeliveryViewSet(viewsets.ModelViewSet):
    queryset = Delivery.objects.select_related('user').all()
    serializer_class = DeliverySerializer
    authentication_classes = [URLTokenAuthentication]
    pagination_class = StandardResultsSetPagination  
    permission_classes = [AllowAny]

    def send_telegram_notification(self, telegram_id, message):
        BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        data = {"chat_id": telegram_id, "text": message}
        requests.post(url, json=data)


class DriverLocationAPIView(APIView):
    authentication_classes = [URLTokenAuthentication]
    permission_classes = [AllowAny]

    def get(self, request, delivery_id):
        try:
            delivery = Delivery.objects.get(id=delivery_id)
            return Response({"latitude": delivery.driver_lat, "longitude": delivery.driver_lon})
        except Delivery.DoesNotExist:
            return Response({"error": "Yetkazib beruvchi topilmadi"}, status=404)


class RouteAPIView(APIView):
    authentication_classes = [URLTokenAuthentication]
    permission_classes = [AllowAny]

    def post(self, request):
        driver_location = request.data.get("driver_location")
        customer_location = request.data.get("customer_location")

        if not driver_location or not customer_location:
            return Response({"error": "Manzillar to‘liq emas"}, status=status.HTTP_400_BAD_REQUEST)

        route_data = get_route(driver_location, customer_location)
        return Response(route_data, status=status.HTTP_200_OK)
