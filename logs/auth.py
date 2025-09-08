from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import APIKey

class APIKeyAuth(BaseAuthentication):
    def authenticate(self, request):
        api_key = request.headers.get("API-KEY")
        if not api_key:
            raise AuthenticationFailed("API key required")
        
        try:
            key_obj = APIKey.objects.get(key=api_key, active=True)
        except APIKey.DoesNotExist:
            raise AuthenticationFailed("Invalid or inactive API key")
        
        return (key_obj.user, key_obj)