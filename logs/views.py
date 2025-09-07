from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import LogEvent
from .serializers import LogEventSerializer
from kafka import KafkaProducer
import json
from django.core.cache import cache

class LogEventView(APIView):
    def post(self, request):
        api_key = request.headers.get('API-KEY')
        if not api_key:
            return Response({"error": "API key required"},
                            status=status.HTTP_400_BAD_REQUEST)
        
        rate_limit_key = f"rate_limit:{api_key}"
        request_count = cache.get(rate_limit_key, 0)

        if request_count >= 100:
            return Response({"error": "Rate limit exceeded"},
                            status=status.HTTP_429_TOO_MANY_REQUESTS)
        
        cache.set(rate_limit_key, request_count+1, timeout=60)

        serializer = LogEventSerializer(data=request.data)
        if serializer.is_valid():
            producer = KafkaProducer(bootstrap_servers='localhost:9092',
                                     value_serializer=lambda v:
                                     json.dumps(v).encode('utf-8'))
            producer.send('log_events', serializer.validated_data)
            producer.flush()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)