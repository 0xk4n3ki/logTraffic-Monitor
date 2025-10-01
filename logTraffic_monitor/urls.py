from django.urls import path, include
from logs.views import SignupView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('', include('django_prometheus.urls')),
    path('api/', include('logs.urls')),
    path('api/auth/signup/', SignupView.as_view(), name="signup"),
    path('api/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
