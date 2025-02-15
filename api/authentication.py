from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from api.models import Tokens  # Token modelingiz shu joyda saqlangan bo'lishi kerak

class URLTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        """
        URL orqali yuborilgan tokenni tekshirish.
        """
        token = request.parser_context.get('kwargs', {}).get('token')

        if not token:
            return None  # Agar token berilmagan bo'lsa, davom ettiradi

        try:
            token_obj = Tokens.objects.get(token=token)  # Tokenni tekshiramiz
            return (token_obj, None)  # Token to‘g‘ri bo‘lsa, foydalanuvchiga ruxsat
        except Tokens.DoesNotExist:
            raise AuthenticationFailed("Noto‘g‘ri token!")

    def authenticate_header(self, request):
        return 'Token'
