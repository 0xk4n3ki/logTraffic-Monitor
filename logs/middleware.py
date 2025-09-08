import time
from django.http import JsonResponse
from django.core.cache import cache
from rest_framework import status
from .models import APIKey

class RateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.path.startswith("/api/logs"):
            return self.get_response(request)
        
        api_key = request.headers.get("API-KEY")
        if not api_key:
            return JsonResponse({"error": "API key required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            key_obj = APIKey.objects.get(key=api_key, active=True)
        except APIKey.DoesNotExist:
            return JsonResponse({"error":"Invalid or inactive API key"}, status=status.HTTP_401_UNAUTHORIZED)
        

        current_minute = int(time.time()//60)
        redis_key = f"rate_limit:{api_key}:{current_minute}"
        request_count = cache.get(redis_key, 0)
        
        if request_count >= 100:
            return JsonResponse({"error":"Rate limit exceeded"}, status=status.HTTP_429_TOO_MANY_REQUESTS)
        
        cache.set(redis_key, request_count+1, timeout=60)
        return self.get_response(request)