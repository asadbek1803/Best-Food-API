# from rest_framework.authentication import BaseAuthentication
# from rest_framework.exceptions import AuthenticationFailed
# from api.models import Tokens  # Token modelingiz shu joyda saqlangan bo'lishi kerak

# class URLTokenAuthentication(BaseAuthentication):
#     def authenticate(self, request):
#         """
#         URL orqali yuborilgan tokenni tekshirish.
#         """
#         token = request.parser_context.get('kwargs', {}).get('token')

#         if not token:
#             return None  # Agar token berilmagan bo'lsa, davom ettiradi

#         try:
#             token_obj = Tokens.objects.get(token=token)  # Tokenni tekshiramiz
#             return (token_obj, None)  # Token to‘g‘ri bo‘lsa, foydalanuvchiga ruxsat
#         except Tokens.DoesNotExist:
#             raise AuthenticationFailed("Noto‘g‘ri token!")

#     def authenticate_header(self, request):
#         return 'Token'

from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import AnonymousUser
from .models import User, Tokens

class URLTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.parser_context['kwargs'].get('token')  # URL'dan token olish
        if not token:
            raise AuthenticationFailed("Token talab qilinadi!")  # Token yo'q bo‘lsa xatolik
        
        if not Tokens.objects.filter(token=token).exists():
            raise AuthenticationFailed("Noto'g'ri token!")  # Token bazada mavjud emas

        return (AnonymousUser(), None)  # Foydalanuvchini autentifikatsiya qilmaymiz