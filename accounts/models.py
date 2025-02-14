from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True, blank=True, null=True)
    is_verified = models.BooleanField(default=False)  # Telefon raqami tasdiqlangan yoki yo'qligi

    def __str__(self):
        return self.username
