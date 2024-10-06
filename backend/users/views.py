# django imports
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, redirect

# rest_framework imports
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

# knox imports
from knox.auth import TokenAuthentication
from knox.views import LoginView as KnoxLoginView
from knox.models import AuthToken

# app imports
from users.models import CustomUser
from users.serializers import CustomUserSerializer, CustomLoginSerializer


# Create your views here.
# -----------------------------------------

def index(request):
    return render(request=request, template_name='users/index.html')

# NOT WORKING
class RootAPIView(APIView):
    def get(self, request):
        return Response({
            "register": reverse('users:register', request=request),
        })


class RegistrationView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = CustomUserSerializer

    def get(self, request):
        return Response({}, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = CustomUserSerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                user = serializer.create(serializer.validated_data)
                # temporarily skip email verification
            except Exception as e:
                print("\n==> ", e)
                return Response({'message': "Error occurred."}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'message': "Thank you."}, status=status.HTTP_201_CREATED)
        return Response({'message': "Serializer not valid."}, status=status.HTTP_400_BAD_REQUEST)
            
class CustomLoginView(KnoxLoginView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [AllowAny]
    serializer_class = CustomLoginSerializer

    def get(self, request):
        return Response({}, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        try:
            access_token = AuthToken.objects.create(user)[1]
            refresh_token = AuthToken.objects.create(user)[1]
        except Exception as e:
            print("\n==>", e)
            return Response({"message": "Error in generating token."})
        if user:
            return Response({
                "user": user.email,
                "access_token": access_token,
                "refresh_token": refresh_token,
            }, status=status.HTTP_200_OK)
        return Response({'message': "Error in user object."})
        