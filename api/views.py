from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .authentication import URLTokenAuthentication
from .models import User, Category, Product, Cart, Delivery, Rating
from .serializers import UserSerializer, CategorySerializer, ProductSerializer, CartSerializer, DeliverySerializer, RatingSerializer
from rest_framework.pagination import PageNumberPagination
from utils.graphhopper import get_route
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10  # Sahifada nechta obyekt chiqishini sozlash
    page_size_query_param = 'page_size'  # URL orqali sahifa o‘lchamini o‘zgartirish uchun
    max_page_size = 100  # Maksimal sahifa o‘lchami

class UserViewSet(viewsets.ModelViewSet):  # Faqat o‘qish mumkin
    queryset = User.objects.all()
    lookup_field = "telegram_id"
    serializer_class = UserSerializer
    authentication_classes = [URLTokenAuthentication]
    permission_classes = [AllowAny]
    pagination_class = StandardResultsSetPagination

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    lookup_field = "name"
    serializer_class = CategorySerializer
    authentication_classes = [URLTokenAuthentication]
    permission_classes = [AllowAny]
    pagination_class = StandardResultsSetPagination

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related('category').all()  # category bilan birga olish
    filterset_fields = ['category']
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    serializer_class = ProductSerializer
    authentication_classes = [URLTokenAuthentication]
    permission_classes = [AllowAny]
    pagination_class = StandardResultsSetPagination

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.select_related('user', 'product').all()
    serializer_class = CartSerializer
    authentication_classes = [URLTokenAuthentication]
    permission_classes = [AllowAny]
    pagination_class = StandardResultsSetPagination

class DeliveryViewSet(viewsets.ModelViewSet):
    queryset = Delivery.objects.select_related('user').all()
    serializer_class = DeliverySerializer
    authentication_classes = [URLTokenAuthentication]
    permission_classes = [AllowAny]
    pagination_class = StandardResultsSetPagination

class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.select_related('user', 'delivery').all()
    serializer_class = RatingSerializer
    authentication_classes = [URLTokenAuthentication]
    permission_classes = [AllowAny]
    pagination_class = StandardResultsSetPagination


class RouteView(APIView):
    """
    Haydovchining yo‘nalishini mijoz manziliga chizish.
    """
    permission_classes = [AllowAny]
    authentication_classes = [URLTokenAuthentication]
    
    def post(self, request):
        driver_location = request.data.get("driver_location")  # [lat, lon]
        customer_location = request.data.get("customer_location")  # [lat, lon]

        if not driver_location or not customer_location:
            return Response({"error": "Manzillar to‘liq emas"}, status=400)

        route_data = get_route(driver_location, customer_location)
        return Response(route_data)