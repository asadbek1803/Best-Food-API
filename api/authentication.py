from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import AnonymousUser
from .models import Tokens  # To'g'ri modelni import qilish

class URLTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        """
        1. URL orqali token olishga harakat qiladi.
        2. Agar token bazada bo'lsa, autentifikatsiyani muvaffaqiyatli bajaradi.
        3. Aks holda AuthenticationFailed xatosini chiqaradi.
        """
        token = request.parser_context.get('kwargs', {}).get('token')

        if token:
            try:
                token_obj = Tokens.objects.get(token=token)
                return (AnonymousUser(), None)  # Token to‘g‘ri bo‘lsa, foydalanuvchini anonim qilib qaytaramiz
            except Tokens.DoesNotExist:
                raise AuthenticationFailed("Noto‘g‘ri yoki mavjud bo‘lmagan token!")

        return None  # Token bo'lmasa autentifikatsiya talab qilinmaydi

    def authenticate_header(self, request):
        """
        401 Unauthorized javobi uchun `WWW-Authenticate` headerni qaytaradi.
        """
        return 'Token'
