from django.urls import path
from .views import LogEventView, LogSearchview, CreateAPIKeyView, ListAPIKeyView

urlpatterns = [
    path('logs/', LogEventView.as_view(), name='log-event'),
    path('logs/search/', LogSearchview.as_view(), name="log-search"),

    path('key/', CreateAPIKeyView.as_view(), name='create-api-key'),
    path('keys/list/', ListAPIKeyView.as_view(), name='list-api-keys'),
]