from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import AnonymousUser
from .models import Tokens
from django.contrib.auth.models import User as user


class URLTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # 1. Agar foydalanuvchi login qilgan bo‘lsa, autentifikatsiya qilish
        if request.user and request.user.is_authenticated:
            return (request.user, None)  

        # 2. Agar foydalanuvchi login qilmagan bo‘lsa, URL orqali tokenni olish
        token = request.parser_context['kwargs'].get('token')
        if not token:
            raise AuthenticationFailed("Token talab qilinadi yoki foydalanuvchi login qilishi kerak!")  

        # 3. Tokenni bazadan tekshirish
        try:
            token_obj = Tokens.objects.select_related("user").get(token=token)
            return (token_obj.user, None)  # Token egasi bo‘lgan foydalanuvchini qaytarish
        except Tokens.DoesNotExist:
            raise AuthenticationFailed("Noto‘g‘ri token!")

        # 4. Ikkala shart ham bajarilmasa
        return None  
