from django.contrib import admin
from .models import User, Category, Product, Cart, Delivery, Rating, Tokens

admin.site.register(Tokens)
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'username', 'telegram_id', 'role', 'created_at')
    search_fields = ('full_name', 'username', 'telegram_id')
    list_filter = ('role', 'created_at')
    ordering = ('-created_at',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'created_at')
    search_fields = ('name',)
    list_filter = ('is_active', 'created_at')
    ordering = ('-created_at',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'is_available', 'created_at')
    search_fields = ('name', 'category__name')
    list_filter = ('is_available', 'category')
    ordering = ('-created_at',)

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'created_at')
    search_fields = ('user__full_name', 'product__name')
    ordering = ('-created_at',)

@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_amount', 'status', 'created_at', 'delivered_at')
    search_fields = ('user__full_name', 'delivery_address')
    list_filter = ('status', 'created_at')
    ordering = ('-created_at',)

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'delivery', 'rating', 'created_at')
    search_fields = ('user__full_name',)
    list_filter = ('rating', 'created_at')
    ordering = ('-created_at',)
