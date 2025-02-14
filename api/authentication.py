from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import AnonymousUser
from .models import Tokens

class URLTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # Agar user allaqachon login qilgan bo'lsa, to'g'ridan-to'g'ri qaytarish
        if getattr(request, "user", None) and getattr(request.user, "is_authenticated", False):
            return (request.user, None)

        # URL orqali token olish
        token = request.parser_context['kwargs'].get('token')
        if not token:
            return None  # Token yo‘q bo‘lsa, autentifikatsiya qilmasdan qaytish

        # Tokenni tekshirish
        try:
            token_obj = Tokens.objects.select_related("user").get(token=token)
            return (token_obj.user, None)
        except Tokens.DoesNotExist:
            raise AuthenticationFailed("Noto‘g‘ri token!")

        return None
