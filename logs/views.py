from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import LogEvent, APIKey
from .serializers import LogEventSerializer, SignupSerializer
from kafka import KafkaProducer
import json
from django.core.cache import cache
from rest_framework.permissions import IsAuthenticated, AllowAny
from .auth import APIKeyAuth
from datetime import datetime
from .tasks import consumer_kafka_logs

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    linger_ms=5,
    acks='all',
)

class LogEventView(APIView):
    authentication_classes = [APIKeyAuth]
    permission_classes = []

    def post(self, request):
        serializer = LogEventSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data.copy()

            for key, value in data.items():
                if isinstance(value, datetime):
                    data[key] = value.isoformat()
            producer.send('log_events', data)

            consumer_kafka_logs.delay()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CreateAPIKeyView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request): 
        name = request.data.get("name") 
        api_key = APIKey.objects.create(user=request.user, name=name) 
        return Response({"api_key":api_key.key}, status=status.HTTP_201_CREATED)

class ListAPIKeyView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        keys = request.user.api_keys.all().values("name", "key", "active", "created_at")
        return Response(keys, status=status.HTTP_200_OK)
    
class SignupView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):

        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"User created successfully"}, status=status.HTTP_201_CREATED)
        

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    