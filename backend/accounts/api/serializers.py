from django.urls import reverse
from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework import serializers
from accounts.models import CustomUser
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import smart_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from accounts.utils.email import send_normal_email
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError


class UserRegisterSerializer(ModelSerializer):
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)
    password2 = serializers.CharField(
        max_length=68, min_length=6, write_only=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'password', 'password2']

    def validate(self, attrs):
        password = attrs.get('password', '')
        password2 = attrs.get('password2', '')
        if password != password2:
            raise serializers.ValidationError("Passwords do not match.")
        return attrs

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            password=validated_data.get('password'),
        )
        return user
    

class UserOTPSerializer(Serializer):
    otp = serializers.IntegerField(max_value=999999, min_value=100000, required=True)


class LoginSerializer(ModelSerializer):
    email = serializers.EmailField(max_length=225, min_length=6)
    password = serializers.CharField(max_length=68, write_only=True)
    full_name = serializers.CharField(max_length=225, read_only=True)
    access_token = serializers.CharField(max_length=225, read_only=True)
    refresh_token = serializers.CharField(max_length=225, read_only=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'full_name', 'access_token', 'refresh_token']

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        request = self.context.get('request')
        user = authenticate(request, email=email, password=password)
        if not user:
            # test this
            raise AuthenticationFailed("Invalid credentials, try again.")
        if not user.is_verified:
            # test this
            raise AuthenticationFailed("Email is not verified.")
        
        user_tokens = user.tokens()
        
        return {
            'email': user.email,
            'full_name': user.get_full_name,
            'access_token': str(user_tokens.get('access')),
            'refresh_token': str(user_tokens.get('refresh')),
        }
    

class LogoutUserSerializer(Serializer):
    refresh_token = serializers.CharField()
    default_error_messages = {
        'bad_token': ('Token is invalid or has expired.')
    }

    def validate(self, attrs):
        self.token = attrs.get('refresh_token')
        return attrs
    
    def save(self, *args, **kwargs):
        try:
            token = RefreshToken(self.token)
            token.blacklist()
        except TokenError:
            return self.fail('bad_token')
        
class PasswordResetRequestSerializer(Serializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email')
        if CustomUser.objects.filter(email=email).exists():
            user = CustomUser.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            request = self.context.get('request')
            site_domain = get_current_site(request).domain
            relative_link = reverse('accounts:password_reset_confirm', kwargs={ 'uidb64': uidb64, 'token': token })
            abslink = f'http://{site_domain}{relative_link}'
            front_link = f'http://localhost:5173/reset-password/{uidb64}/{token}/'
            email_body = f'Hi, Please use the following link to reset your password.\n {abslink}\n or use the front link: \n {front_link}'
            data = {
                'email_body': email_body,
                'email_subject': "Reset your password.",
                'to_email': user.email
            }
            send_normal_email(data)
        else:
            raise serializers.ValidationError("User with email not found.")
        return super().validate(attrs)
    

class SetNewPasswordSerializer(Serializer):
    password = serializers.CharField(max_length=100, min_length=6, write_only=True)
    confirm_password = serializers.CharField(max_length=100, min_length=6, write_only=True)
    uidb64 = serializers.CharField(write_only=True)
    token = serializers.CharField(write_only=True)

    class Meta:
        fields = ['password', 'confirm_password', 'uidb64', 'token']

    def validate(self, attrs):
        try:
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')
            password = attrs.get('password')
            confirm_password=attrs.get('confirm_password')

            print("\nTOKEN ====> ", token)

            user_id = force_str(urlsafe_base64_decode(uidb64))
            # force_str similar to smart_str, converts byte string to regular strings
            user = CustomUser.objects.get(id=user_id)
            if PasswordResetTokenGenerator().check_token(user, token) == True:
                print("\nToken GOOD\n")
            else:
                print("\nToken BAD\n")
                raise serializers.ValidationError("Token invalid")
            if password != confirm_password:
                raise serializers.ValidationError("Passwords do not match.")
            user.set_password(password)
            user.save()
            return user
        except Exception as e:
            raise serializers.ValidationError("Validation Failed.")
        

class EditProfileSerializer(Serializer):
    first_name = serializers.CharField(min_length=2, max_length=30, required=False)
    last_name = serializers.CharField(min_length=2, max_length=50, required=False)

class UpdatePasswordSerializer(Serializer):
    current_password = serializers.CharField(min_length=6, required=True)
    new_password = serializers.CharField(min_length=6, required=True)
    repeat_password = serializers.CharField(min_length=6, required=True)

    def validate(self, attrs):
        if attrs.get('new_password') != attrs.get('repeat_password'):
            raise serializers.ValidationError("New Passwords do not match.")
        return attrs