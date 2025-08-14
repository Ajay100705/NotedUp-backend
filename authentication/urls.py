from django.urls import path
from .views import (
    RegisterView, ProfileView, ChangePasswordView,
    UpgradeUserView, VerifyEmailView
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # Auth
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Email verification
    path('verify-email/<int:uid>/<str:token>/', VerifyEmailView.as_view(), name='verify_email'),

    # User actions
    path('profile/', ProfileView.as_view(), name='profile'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),

    # Admin
    path('users/<int:user_id>/upgrade/', UpgradeUserView.as_view(), name='upgrade_user'),
]
