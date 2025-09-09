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
from elasticsearch import Elasticsearch
from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder
from functools import lru_cache

es = Elasticsearch([settings.ELASTICSEARCH_HOST])


@lru_cache(maxsize=1)
def get_producer():
    return KafkaProducer(
    bootstrap_servers=[settings.KAFKA_BROKER_URL],
    value_serializer=lambda v: json.dumps(v, cls=DjangoJSONEncoder).encode('utf-8'),
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

            # for key, value in data.items():
            #     if isinstance(value, datetime):
            #         data[key] = value.isoformat()

            # get_producer().send('log_events', data)
            producer = get_producer()
            producer.send("log_events", data)
            producer.flush()

            # consumer_kafka_logs.delay()
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
    

class LogSearchview(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        service = request.query_params.get('service')
        level = request.query_params.get('level')
        start = request.query_params.get('start')
        end = request.query_params.get('end')
        page = int(request.query_params.get('page', 1))
        size = 10
        offset = (page-1)*size

        must = []
        if service:
            must.append({"match":{"service_name":service}})
        if level:
            must.append({"match":{"log_level":level}})
        if start and end:
            must.append({
                "range": {
                    "timestamp": {
                        "gte":start,
                        "lte": end
                    }
                }
            })
        query = {"query": {"bool": {"must": must}}}

        results = es.search(index="logs", body=query, from_=offset, size=size)
        hits = [hit["_source"] for hit in results["hits"]["hits"]]

        return Response({
            "page": page,
            "total": results["hits"]["total"]["value"],
            "results": hits
        }, status=status.HTTP_200_OK)