import random
from time import sleep
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import User, VerificationCode
from .serializers import UserSerializer, VerificationCodeSerializer


class PhoneAuthView(APIView):
    @swagger_auto_schema(
        operation_description="Authenticate user by phone number",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'phone_number': openapi.Schema(type=openapi.TYPE_STRING, description='User phone number')
            }
        ),
        responses={200: openapi.Response('Code sent', VerificationCodeSerializer)}
    )
    def post(self, request):
        phone_number = request.data.get('phone_number')
        if not phone_number:
            return Response({"error": "Phone number is required"}, status=status.HTTP_400_BAD_REQUEST)

        user, created = User.objects.get_or_create(phone_number=phone_number)

        code = str(random.randint(1000, 9999))

        VerificationCode.objects.create(user=user, code=code)

        return Response({"message": "Code sent", "is_new_user": created, "code": code}, status=status.HTTP_200_OK)


class VerifyCodeView(APIView):
    @swagger_auto_schema(
        operation_description="Verify user by code",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'phone_number': openapi.Schema(type=openapi.TYPE_STRING, description='User phone number'),
                'code': openapi.Schema(type=openapi.TYPE_STRING, description='Verification code')
            }
        ),
        responses={200: 'Verification successful'}
    )
    def post(self, request):
        phone_number = request.data.get('phone_number')
        code = request.data.get('code')

        try:
            valid_code = VerificationCode.objects.get(user__phone_number=phone_number, code=code)
        except VerificationCode.DoesNotExist:
            return Response({"error": "Invalid code"}, status=status.HTTP_400_BAD_REQUEST)

        if valid_code.is_valid():
            valid_code.is_used = True
            valid_code.save()
            user = User.objects.filter(phone_number=phone_number).first()
            if user:
                return Response({"message": "Verification successful"}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid code"}, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    """
    Retrieve or update a user's profile.
    """

    @swagger_auto_schema(
        operation_description="Get user profile by phone number",
        responses={200: UserSerializer},
        manual_parameters=[
            openapi.Parameter('phone_number', openapi.IN_QUERY, description="Phone number of the user", type=openapi.TYPE_STRING)
        ]
    )
    def get(self, request):
        phone_number = request.data.get('phone_number')
        user = User.objects.filter(phone_number=phone_number).first()
        if not user:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user)
        return Response(serializer.data)


class ActivateInviteView(APIView):
    @swagger_auto_schema(
        operation_description="Activate invite code for user",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'phone_number': openapi.Schema(type=openapi.TYPE_STRING, description='User phone number'),
                'invite_code': openapi.Schema(type=openapi.TYPE_STRING, description='Invite code to activate')
            }
        ),
        responses={200: 'Invite code activated'}
    )
    def post(self, request):
        phone_number = request.data.get('phone_number')
        invite_code = request.data.get('invite_code')

        user = User.objects.filter(phone_number=phone_number).first()
        if not user:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        if user.activated_invite:
            return Response({"message": "Invite code already activated", "activated_invite": user.activated_invite})

        inviter = User.objects.filter(invite_code=invite_code).first()
        if not inviter:
            return Response({"error": "Invalid invite code"}, status=status.HTTP_400_BAD_REQUEST)

        user.activated_invite = invite_code
        inviter.referred_users.add(user)
        user.save()

        return Response({"message": "Invite code activated"})
