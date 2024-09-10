from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse
from accounts.serializers import (
    UserRegisterSerializer,
    UserOTPSerializer,
    LoginSerializer,
    LogoutUserSerializer
)
from rest_framework.generics import GenericAPIView
from rest_framework import status
from utils.email import send_code_to_user
from accounts.models import OneTimePassword
from rest_framework.permissions import IsAuthenticated

# Create your views here.


class AccountsIndexView(APIView):
    def get(self, request):
        return Response({
            "register": reverse('accounts:register', request=request),
            "verify-email": reverse('accounts:verify_email', request=request),
            "login": reverse('accounts:login', request=request),
            "auth-required": reverse('accounts:auth_required', request=request),
            "refresh_token": reverse('accounts:refresh_token', request=request)
        })


class RegisterUserView(GenericAPIView):
    serializer_class = UserRegisterSerializer

    def post(self, request):
        user_data = request.data
        serializer = self.serializer_class(data=user_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user = serializer.data
            send_code_to_user(user['email'])
            return Response({
                'data': user,
                'message': f'Hi, thanks for signing up. please check your email.',
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyUserEmail(GenericAPIView):
    serializer_class = UserOTPSerializer

    def post(self, request):
        otpcode = request.data.get('otp')
        try:
            user_code_obj = OneTimePassword.objects.get(code=otpcode)
            user = user_code_obj.user
            if not user.is_verified:
                user.is_verified = True
                user.save()
                return Response({
                    'message': 'Email account verified successfully, Thank you.',
                }, status=status.HTTP_200_OK)
            return Response({
                'message': 'Code is invalid/expired or user is already verified.'
            }, status=status.HTTP_204_NO_CONTENT)
        except OneTimePassword.DoesNotExist:
            return Response({'message': 'This code was not provided.'}, status=status.HTTP_404_NOT_FOUND)


class LoginUserView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class TestAuthenticationView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        return Response({ "msg": "Hooooooooooooooooray!!!" }, status=status.HTTP_200_OK)
    

class LogoutUserView(GenericAPIView):
    serializer_class = LogoutUserSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"msg": "Logout successful, token blacklisted."}, status=status.HTTP_200_OK)