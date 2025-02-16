from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from .models import Order, Delivery, Product, Rating, OrderItem
from .serializers import OrderSerializer, DeliverySerializer, OrderItemSerializer, UserSerializer, ProductSerializer, RatingSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from django.db.models import Sum, Count
from datetime import datetime, timedelta
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, get_user_model
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView

user = get_user_model()


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class OrderItemsViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    lookup_field = "id"
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    pagination_class = StandardResultsSetPagination    

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    lookup_field = "telegram_id"
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    pagination_class = StandardResultsSetPagination    


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [OrderingFilter]
    ordering_fields = ["created_at", "total_amount"]
    ordering = ["-created_at"]

    def get_queryset(self):
        return Order.objects.all().order_by("-created_at")  # ✅ To‘g‘ri


class AdminLoginAPIView(APIView):
    """
    Admin foydalanuvchilar uchun login API.
    Foydalanuvchi login va parolni jo‘natadi va JWT tokenlar oladi.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)

        if user is not None and user.is_staff:  # Faqat adminlarni kiritamiz
            refresh = RefreshToken.for_user(user)
            return Response({
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            }, status=status.HTTP_200_OK)

        return Response({"error": "Noto‘g‘ri login yoki parol"}, status=status.HTTP_400_BAD_REQUEST)

class AdminLogoutAPIView(APIView):
    """
    Admin foydalanuvchilar uchun logout API.
    Refresh tokenni qora ro‘yxatga tushiradi.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response({"error": "Refresh token talab qilinadi!"}, status=status.HTTP_400_BAD_REQUEST)
            
            token = RefreshToken(refresh_token)
            token.blacklist()  # Refresh tokenni qora ro‘yxatga tushiramiz

            return Response({"message": "Chiqish muvaffaqiyatli bajarildi"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class AdminTokenRefreshView(TokenRefreshView):
    """
    Admin foydalanuvchilar uchun token yangilash API.
    Foydalanuvchi refresh tokenni jo‘natadi va yangi access token oladi.
    """
    permission_classes = [AllowAny]


class AdminProfileAPIView(APIView):
    """
    Admin foydalanuvchi o‘z profil ma'lumotlarini olish API.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        data = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "is_staff": user.is_staff,
            "is_superuser": user.is_superuser,
        }
        return Response(data, status=status.HTTP_200_OK)



class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated, IsAdminUser]


class DeliveryViewSet(viewsets.ModelViewSet):
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated, IsAdminUser]


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    serializer_class = RatingSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated, IsAdminUser]


class SalesStatisticsAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        today = datetime.today()
        start_of_month = today.replace(day=1)
        
        total_sales = Order.objects.aggregate(total=Sum('total_amount'))['total'] or 0
        total_orders = Order.objects.count()

        last_month = start_of_month - timedelta(days=1)
        start_of_last_month = last_month.replace(day=1)

        last_month_sales = Order.objects.filter(created_at__range=[start_of_last_month, last_month]).aggregate(total=Sum('total_amount'))['total'] or 0
        monthly_change = ((total_sales - last_month_sales) / last_month_sales * 100) if last_month_sales else 0

        data = {
            "total_sales": total_sales,
            "monthly_change": round(monthly_change, 2),
            "total_expenses": 0,
            "total_orders": total_orders,
            "total_customers": 0,
            "refunds": 0,
        }
        
        return Response(data)
