from django.urls import path
from .views import LogEventView, CreateAPIKeyView, ListAPIKeyView

urlpatterns = [
    path('logs/', LogEventView.as_view(), name='log-event'),

    path('key/', CreateAPIKeyView.as_view(), name='create-api-key'),
    path('keys/list/', ListAPIKeyView.as_view(), name='list-api-keys'),
]