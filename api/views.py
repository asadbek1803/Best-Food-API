from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from .authentication import URLTokenAuthentication
from .models import User, Category, Product, Cart, Delivery, Rating, Order
from .serializers import UserSerializer, CategorySerializer, ProductSerializer, OrderSerializer, CartSerializer, DeliverySerializer, RatingSerializer
from rest_framework.pagination import PageNumberPagination
from utils.graphhopper import get_route
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from django.utils.timezone import now
from django.core.files.base import ContentFile
import requests
import base64
from django.db.models import Sum, Count
from datetime import datetime, timedelta



class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class UserViewSet(viewsets.ModelViewSet):
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


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.select_related('user', 'delivery').all()
    serializer_class = OrderSerializer
    authentication_classes = [URLTokenAuthentication]
    permission_classes = [AllowAny]
    pagination_class = StandardResultsSetPagination


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related('category').all()
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

    @action(detail=True, methods=['POST'])
    def update_status(self, request, pk=None):
        """
        Buyurtma holatini yangilash (haydovchi yoki admin tomonidan)
        """
        delivery = self.get_object()
        status = request.data.get("status")

        if status not in ['pending', 'accepted', 'delivered', 'cancelled']:
            return Response({"error": "Noto‘g‘ri holat"}, status=status.HTTP_400_BAD_REQUEST)

        delivery.status = status
        delivery.delivered_at = now() if status == 'delivered' else None
        delivery.save()

        # Telegram botga xabar yuborish
        self.send_telegram_notification(delivery.user.telegram_id, f"Sizning buyurtmangiz: {status}")

        return Response({"message": "Buyurtma holati yangilandi"}, status=status.HTTP_200_OK)

    def send_telegram_notification(self, telegram_id, message):
        """
        Telegram bot orqali foydalanuvchiga xabar yuborish
        """
        BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        data = {"chat_id": telegram_id, "text": message}
        requests.post(url, json=data)


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.select_related('user', 'delivery').all()
    serializer_class = RatingSerializer
    authentication_classes = [URLTokenAuthentication]
    permission_classes = [AllowAny]
    pagination_class = StandardResultsSetPagination


class DriverLocationAPIView(APIView):
    def get(self, request, delivery_id):
        try:
            delivery = Delivery.objects.get(id=delivery_id)
            return Response({"latitude": delivery.driver_lat, "longitude": delivery.driver_lon})
        except Delivery.DoesNotExist:
            return Response({"error": "Yetkazib beruvchi topilmadi"}, status=404)
        



class RouteAPIView(APIView):
    """
    Haydovchi va mijoz joylashuvi asosida yo‘nalishni hisoblash
    """
    permission_classes = [AllowAny]

    def post(self, request):
        driver_location = request.data.get("driver_location")
        customer_location = request.data.get("customer_location")

        if not driver_location or not customer_location:
            return Response({"error": "Manzillar to‘liq emas"}, status=status.HTTP_400_BAD_REQUEST)

        route_data = get_route(driver_location, customer_location)
        return Response(route_data, status=status.HTTP_200_OK)


class DriverLocationUpdate(APIView):
    """
    Haydovchining oxirgi joylashuvini saqlash
    """
    authentication_classes = [URLTokenAuthentication]
    permission_classes = [AllowAny]

    def post(self, request):
        user = request.user
        if user.role != "driver":
            return Response({"error": "Faqat haydovchilar jo‘natishi mumkin"}, status=status.HTTP_403_FORBIDDEN)

        latitude = request.data.get("latitude")
        longitude = request.data.get("longitude")

        if not latitude or not longitude:
            return Response({"error": "Koordinatalar to‘liq emas"}, status=status.HTTP_400_BAD_REQUEST)

        Delivery.objects.filter(user=user, status='accepted').update(
            location_latitude=latitude,
            location_longitude=longitude
        )

        return Response({"message": "Joylashuv yangilandi"}, status=status.HTTP_200_OK)


class PaymentUploadAPIView(APIView):
    """
    To‘lov uchun tasdiqlash rasmi yuklash
    """
    authentication_classes = [URLTokenAuthentication]
    permission_classes = [AllowAny]

    def post(self, request, pk=None):
        delivery = Delivery.objects.get(pk=pk)
        image_data = request.data.get("pay_image")

        if not image_data:
            return Response({"error": "Rasm mavjud emas"}, status=status.HTTP_400_BAD_REQUEST)

        format, imgstr = image_data.split(';base64,')
        ext = format.split('/')[-1]
        delivery.pay_image.save(f"payment_{delivery.id}.{ext}", ContentFile(base64.b64decode(imgstr)))
        delivery.save()

        return Response({"message": "To‘lov tasdiqlandi"}, status=status.HTTP_200_OK)


class OrderStatusAPIView(APIView):
    authentication_classes = [URLTokenAuthentication]
    permission_classes = [AllowAny]
    pagination_class = StandardResultsSetPagination
    def post(self, request, order_id):
        status = request.data.get("status")
        if not status:
            return Response({"error": "Holat talab qilinadi"}, status=400)

        try:
            order = Order.objects.get(id=order_id)
            order.status = status
            order.save()
            return Response({"message": "Buyurtma holati yangilandi"})
        except Order.DoesNotExist:
            return Response({"error": "Buyurtma topilmadi"}, status=404)



class SalesStatisticsAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        today = datetime.today()
        start_of_month = today.replace(day=1)
        
        total_sales = Order.objects.aggregate(total=Sum('total_amount'))['total'] or 0
        total_orders = Order.objects.count()

        # Oylik o'zgarish
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
            "refunds": 0,  # Hozircha qaytarilgan pullar bo'yicha ma'lumot yo'q
        }
        
        return Response(data)
