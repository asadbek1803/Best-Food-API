from rest_framework import serializers
from .models import User, Category, Product, Cart, Delivery, Rating, Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"


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
    category = CategoryForProduct()
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
