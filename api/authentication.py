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
