from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse
from accounts.serializers import (
    UserRegisterSerializer,
    UserOTPSerializer
)
from rest_framework.generics import GenericAPIView
from rest_framework import status
from utils.email import send_code_to_user
from accounts.models import OneTimePassword

# Create your views here.


class AccountsIndexView(APIView):
    def get(self, request):
        return Response({
            "register": reverse('accounts:register', request=request),
            "verify-email": reverse('accounts:verify_email', request=request)
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
        print(serializer.errors)
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
                    'message': 'account email verified successfully',
                }, status=status.HTTP_200_OK)
            return Response({
                'message': 'code is invalid or user is already verified.'
            }, status=status.HTTP_204_NO_CONTENT)
        except OneTimePassword.DoesNotExist:
            return Response({'message': 'passcode not provided'}, status=status.HTTP_404_NOT_FOUND)
