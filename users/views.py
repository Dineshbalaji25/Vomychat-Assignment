from django.contrib.auth import get_user_model, authenticate
from django.core.mail import send_mail
from django.conf import settings
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from rest_framework import generics, status, views
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import (RegisterSerializer, LoginSerializer, ForgotPasswordSerializer,
                          ReferralSerializer, ReferralStatsSerializer)
from .models import Referral
from .tokens import reset_token_generator

User = get_user_model()

# POST /api/register
class RegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all() 
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    
# POST /api/login
class LoginAPIView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        # Generate JWT token pair
        refresh = RefreshToken.for_user(user)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        })

# POST /api/forgot-password
class ForgotPasswordAPIView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"detail": "User with this email does not exist."},
                            status=status.HTTP_400_BAD_REQUEST)
        # It will generate a password reset token
        token = reset_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        reset_link = f"http://127.0.0.1:8000/reset-password/{uid}/{token}/"  # Replace with your domain name
        send_mail(
            subject="Password Reset",
            message=f"Use this link to reset your password: {reset_link}",
            from_email=settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@yourdomain.com',
            recipient_list=[user.email],
            fail_silently=False,
        )
        return Response({"detail": "Password reset link has been sent to your email."})

# GET /api/referrals
class ReferralListAPIView(generics.ListAPIView):
    serializer_class = ReferralSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Referral.objects.filter(referrer=self.request.user)

# GET /api/referral-stats
class ReferralStatsAPIView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        referrals = Referral.objects.filter(referrer=request.user)
        total = referrals.count()
        successful = referrals.filter(status='successful').count()
        stats = {
            "total_referrals": total,
            "successful_referrals": successful
        }
        serializer = ReferralStatsSerializer(stats)
        return Response(serializer.data)
