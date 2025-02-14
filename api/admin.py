from django.contrib import admin
from .models import User, Tokens, Category, Product, Cart, Order, OrderItem, Delivery, Rating

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'username', 'telegram_id', 'language', 'role', 'is_admin', 'created_at')
    search_fields = ('full_name', 'username', 'telegram_id')
    list_filter = ('role', 'language', 'is_admin')

@admin.register(Tokens)
class TokensAdmin(admin.ModelAdmin):
    list_display = ('name', 'token')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('uz_name', 'ru_name', 'en_name', 'is_active', 'created_at')
    search_fields = ('uz_name', 'ru_name', 'en_name')
    list_filter = ('is_active',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('uz_name', 'ru_name', 'en_name', 'price', 'is_available', 'created_at')
    search_fields = ('uz_name', 'ru_name', 'en_name')
    list_filter = ('is_available', 'category')

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'created_at')
    search_fields = ('user__full_name', 'product__uz_name')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_amount', 'status', 'created_at')
    search_fields = ('user__full_name',)
    list_filter = ('status',)

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity')

@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ('order', 'driver', 'status', 'created_at', 'delivered_at')
    search_fields = ('order__id', 'driver__full_name')
    list_filter = ('status',)

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'delivery', 'rating', 'created_at')
    search_fields = ('user__full_name', 'delivery__order__id')
