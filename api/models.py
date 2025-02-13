from django.db import models

class User(models.Model):
    ROLE = (
        ("user", "Foydalanuvchi"),
        ("driver", "Yetkazib beruvchi"),
        ("cooker", "Oshpaz")
    )
    full_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, null=True, blank=True)
    telegram_id = models.BigIntegerField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    language = models.CharField(max_length=255)
    role = models.CharField(max_length=100, choices=ROLE)

    def __str__(self):
        return self.full_name
    
class Tokens(models.Model):
    name = models.CharField(max_length=100)
    token = models.TextField()
    

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(null=True, blank=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.full_name} - {self.product.name} ({self.quantity})"

class Delivery(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Tayyorlanmoqda'),
        ('accepted', 'Yetkazilmoqda'),
        ('delivered', 'Yetkazildi'),
        ('cancelled', 'Bekor qilindi'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_address = models.TextField()
    location_latitude = models.DecimalField(max_digits=10, decimal_places=8, null=True, blank=True)
    location_longitude = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    pay_image = models.ImageField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    delivered_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Delivery {self.id} - {self.user.full_name}"

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    delivery = models.ForeignKey(Delivery, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'delivery')

    def __str__(self):
        return f"{self.user.full_name} - {self.rating}"
