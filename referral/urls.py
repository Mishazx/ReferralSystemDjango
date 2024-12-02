from django.urls import path
from . import views

urlpatterns = [
    path('auth/', views.PhoneAuthView.as_view(), name='auth'),
    path('verify/', views.VerifyCodeView.as_view(), name='verify'),
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('profile/invite/', views.ActivateInviteView.as_view(), name='invite_profile'),
]
