from django.urls import path
from .views import (
    RegisterAPIView,
    LoginAPIView,
    ForgotPasswordAPIView,
    ReferralListAPIView,
    ReferralStatsAPIView,
)

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='api-register'),
    path('login/', LoginAPIView.as_view(), name='api-login'),
    path('forgot-password/', ForgotPasswordAPIView.as_view(), name='api-forgot-password'),
    path('referrals/', ReferralListAPIView.as_view(), name='api-referrals'),
    path('referral-stats/', ReferralStatsAPIView.as_view(), name='api-referral-stats'),
]
