from django.urls import path
from .views import PhoneAuthView, VerifyCodeView, UserProfileView

urlpatterns = [
    path('auth/', PhoneAuthView.as_view(), name='auth'),
    path('verify/', VerifyCodeView.as_view(), name='verify'),
    path('profile/', UserProfileView.as_view(), name='profile'),
]
