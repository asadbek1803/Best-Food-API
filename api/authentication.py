from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import AnonymousUser
from .models import Tokens


class URLTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        """
        Authenticate using either:
        1. URL token if present
        2. Already authenticated user
        """
        # First check if token is provided in URL
        token = request.parser_context.get('kwargs', {}).get('token')
        
        if token:
            try:
                # Try to get user via token
                token_obj = Tokens.objects.filter(token=token).exists()
                return token_obj
            except Tokens.DoesNotExist:
                raise AuthenticationFailed("Noto'g'ri token!")
        
        # If no token, check if user is already authenticated
        if request.user and request.user.is_authenticated:
            return (request.user, None)
            
        # If neither token nor authenticated user, return None
        # This will allow the request to proceed to permission classes
        return None

    def authenticate_header(self, request):
        """
        Return a string to be used as the value of the `WWW-Authenticate`
        header in a `401 Unauthenticated` response
        """
        return 'Token'