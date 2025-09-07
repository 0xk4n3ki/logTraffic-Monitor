from django.urls import path
from .views import LogEventView

urlpatterns = [
    path('logs/', LogEventView.as_view(), name='log-event')
]