from django.core.validators import validate_email
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.generics import GenericAPIView
from rest_framework import status
from django.http import HttpResponseRedirect
from accounts.utils.email import send_code_to_user, re_verify_email
from accounts.models import OneTimePassword
from rest_framework.permissions import IsAuthenticated
from django.utils.encoding import smart_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from accounts.models import CustomUser
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from accounts.api.serializers import (
    UserRegisterSerializer,
    UserOTPSerializer,
    LoginSerializer,
    LogoutUserSerializer,
    PasswordResetRequestSerializer,
    SetNewPasswordSerializer,
    EditProfileSerializer,
    UpdatePasswordSerializer,
    ChangeEmailSerializer
)

# Create your views here.

# register (ok) (updated)
# verify (ok) (updated)
# login (ok) (updated)
# auth-required (test) (ok)
# password reset request (ok)
# password reset confirm (ok)
# set new password (ok)
# edit profile (ok)
# update password (ok)
# change email
# profile (first/last name + email)

class AccountsIndexView(APIView):
    def get(self, request) -> Response:
        return Response({
            "change-email": reverse('accounts:change_email', request=request),
            "update-password": reverse('accounts:update_password', request=request),
            "register": reverse('accounts:register', request=request),
            "verify-email": reverse('accounts:verify_email', request=request),
            "login": reverse('accounts:login', request=request),
            "auth-required": reverse('accounts:auth_required', request=request),
            "refresh_token": reverse('accounts:refresh_token', request=request),
            "password_reset_request": reverse('accounts:password_reset', request=request),
            "set_new_password": reverse('accounts:set_new_password', request=request),
            "html_index": reverse("accounts:html_index", request=request),
        })


class RegisterUserView(GenericAPIView):
    serializer_class = UserRegisterSerializer

    def get(self, request):
        return Response({}, status=status.HTTP_200_OK)

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
    

class PasswordResetRequestView(GenericAPIView):
    serializer_class = PasswordResetRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        return Response({
            'message': 'A link containing password reset link has been sent to you.'
        }, status=status.HTTP_200_OK)
    

class PasswordResetConfirmView(GenericAPIView):

    def get(self, request, uidb64, token):
        try:
            user_id = smart_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(id=user_id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({
                    'message': "Token is invalid or has expired"
                }, status=status.HTTP_401_UNAUTHORIZED)
            return Response({
                'success': True,
                'message': 'Credentials is valid',
                'uidb64': uidb64,
                'token': token
            }, status=status.HTTP_200_OK)
        except DjangoUnicodeDecodeError:
            return Response({'message': "Token is invalid or has expired"}, status=status.HTTP_401_UNAUTHORIZED)
        

class SetNewPasswordView(GenericAPIView):
    serializer_class = SetNewPasswordSerializer
    
    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({
            'message': 'Password reset successful.'
        }, status=status.HTTP_200_OK)
    

# may require update on self.request.data.get to serializer.get
# REMOVED url
class EditProfileView(GenericAPIView):
    serializer_class = EditProfileSerializer
    permission_classes = [IsAuthenticated]
    def get(self, request):
        return Response({
            'Current First Name': request.user.first_name,
            'Current Last Name': request.user.last_name,
        }, status=status.HTTP_200_OK)
    
    def post(self, request):
        self.user = self.request.user
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            first_name = self.request.data.get('first_name')
            last_name = self.request.data.get('last_name')
            if first_name:
                self.user.first_name = first_name
            else:
                pass
            if last_name:
                self.user.last_name = last_name
            else:
                pass
            self.user.save()
            return HttpResponseRedirect(reverse('accounts:edit_profile'))
        

# OK
class UpdatePasswordView(GenericAPIView):
    serializer_class = UpdatePasswordSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({'message': "Change your password."}, status=status.HTTP_200_OK)
    
    def post(self, request):
        self.user = self.request.user
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            current_password = serializer.data.get('current_password')
            if self.user.check_password(current_password):
                new_password = serializer.data.get('new_password')
                repeat_password = serializer.data.get('repeat_password')
                if new_password == repeat_password:
                    self.user.set_password(new_password)
                    self.user.save()
                    return Response({'message': "success"}, status=status.HTTP_200_OK)
                return Response({'message': 'Passwords do not match.'}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'message': "Current password is incorrect."}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': "failure"}, status=status.HTTP_400_BAD_REQUEST)

# validate email does not work
class ChangeEmailView(GenericAPIView):
    serializer_class = ChangeEmailSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            'message': "Change your email, requires re-verification.",
            'current email': request.user.email,
            'verified': request.user.is_verified
        }, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = self.request.user
            new_email = serializer.data.get('new_email')
            if user.is_verified:
                user.email = new_email
                user.is_verified = False
                user.save()
                re_verify_email(user.id)
                return Response({'message': 'done'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'user is not verified.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'messagee': 'serializer is not valid.'}, status=status.HTTP_400_BAD_REQUEST)