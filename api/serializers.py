from rest_framework import serializers
from .models import User, Category, Product, Cart, Delivery, Rating, Order, OrderItem



from rest_framework import serializers
from .models import User, Category, Product, Cart, Delivery, Rating, Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']

    def get_product(self, obj):
        request = self.context.get('request')
        language = request.query_params.get('lang', 'uz')
        return {
            "id": obj.product.id,
            "name": getattr(obj.product, f"{language}_name", obj.product.uz_name),
            "price": obj.product.price,
            "image": obj.product.image.url if obj.product.image else None
        }


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(source='orderitem_set', many=True, read_only=True)
    customer = serializers.SerializerMethodField()
    status_display = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'customer', 'total_amount', 'status', 'status_display', 'created_at', 'items']

    def get_customer(self, obj):
        return {
            "id": obj.user.id,
            "full_name": obj.user.full_name,
            "username": obj.user.username,
            "telegram_id": obj.user.telegram_id
        }

    def get_status_display(self, obj):
        return obj.get_status_display()


class EmptySerializer(serializers.Serializer):
    pass


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class CategoryForProduct(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('name', )

    def get_name(self, obj):
        request = self.context.get('request')
        language = request.query_params.get('lang', 'uz')  # Default til - O‘zbekcha
        return getattr(obj, f"{language}_name", obj.uz_name)  # Til bo‘yicha chiqarish


class CategorySerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    class Meta:
        model = Category
        exclude = ['uz_name', 'ru_name', 'en_name', 'uz_description', 'ru_description', 'en_description']  

    def get_name(self, obj):
        request = self.context.get('request')
        language = request.query_params.get('lang', 'uz')
        return getattr(obj, f"{language}_name", obj.uz_name)

    def get_description(self, obj):
        request = self.context.get('request')
        language = request.query_params.get('lang', 'uz')
        return getattr(obj, f"{language}_description", obj.uz_description)


class ProductSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    class Meta:
        model = Product
        exclude = ['uz_name', 'ru_name', 'en_name', 'uz_description', 'ru_description', 'en_description']

    def get_name(self, obj):
        request = self.context.get('request')
        language = request.query_params.get('lang', 'uz')
        return getattr(obj, f"{language}_name", obj.uz_name)

    def get_description(self, obj):
        request = self.context.get('request')
        language = request.query_params.get('lang', 'uz')
        return getattr(obj, f"{language}_description", obj.uz_description)


class CartSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = Cart
        fields = "__all__"


class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = "__all__"


class RatingSerializer(serializers.ModelSerializer):
    comment = serializers.SerializerMethodField()

    class Meta:
        model = Rating
        exclude = ['uz_comment', 'ru_comment', 'en_comment']

    def get_comment(self, obj):
        request = self.context.get('request')
        language = request.query_params.get('lang', 'uz')
        return getattr(obj, f"{language}_comment", obj.uz_comment)
