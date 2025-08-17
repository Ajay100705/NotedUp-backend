from django.urls import path
from .views import RegisterView, VerifyEmailView, ProfileView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # Auth
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Email verification
    path('verify-email/<int:uid>/<str:token>/', VerifyEmailView.as_view(), name='verify_email'),

    # Profile
    path('profile/', ProfileView.as_view(), name='profile'),
]
