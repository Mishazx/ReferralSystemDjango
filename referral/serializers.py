from rest_framework import serializers
from django.utils import timezone

from .models import User, VerificationCode


class UserSerializer(serializers.ModelSerializer):
    referred_users = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['phone_number', 'invite_code', 'activated_invite', 'referred_users']

    def get_referred_users(self, obj):
        return obj.referred_users.values_list('phone_number', flat=True)


class VerificationCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VerificationCode
        fields = ['user', 'code', 'created_at', 'expires_at', 'is_used']

    def validate(self, data):
        if data['expires_at'] < timezone.now():
            raise serializers.ValidationError({'code': 'Invalid code'})
        return data