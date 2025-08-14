from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from .models import User
from .serializers import RegisterSerializer, UserSerializer, ChangePasswordSerializer
from .permissions import IsAdmin
from .tokens import email_verification_token

# Register + send verification email
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        token = email_verification_token.make_token(user)
        verify_url = self.request.build_absolute_uri(
            reverse('verify_email', kwargs={'uid': user.id, 'token': token})
        )
        send_mail(
            'Verify your NotedUp account',
            f'Click the link to verify your account:\n{verify_url}',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )

# Email verification
class VerifyEmailView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, uid, token):
        try:
            user = User.objects.get(pk=uid)
        except User.DoesNotExist:
            return Response({"error": "Invalid verification link"}, status=400)

        if email_verification_token.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({"message": "Email verified successfully"}, status=200)
        return Response({"error": "Invalid or expired token"}, status=400)

# Profile view
class ProfileView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

# Change password
class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, queryset=None):
        return self.request.user

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.request.user.set_password(serializer.validated_data['new_password'])
        self.request.user.save()
        return Response({"message": "Password updated successfully"}, status=status.HTTP_200_OK)

# Admin: upgrade student to uploader
class UpgradeUserView(APIView):
    permission_classes = [IsAdmin]

    def post(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        if user.role == 'admin':
            return Response({"error": "Cannot change role of another admin"}, status=400)
        user.role = 'uploader'
        user.save()
        return Response({"message": f"{user.username} upgraded to uploader"}, status=200)
