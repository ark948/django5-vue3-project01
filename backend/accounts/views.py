from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse
from accounts.serializers import (
    UserRegisterSerializer
)
from rest_framework.generics import GenericAPIView
from rest_framework import status
from utils.email import send_code_to_user

# Create your views here.

class AccountsIndexView(APIView):
    def get(self, request):
        return Response({
            "register": reverse('accounts:register', request=request)
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
