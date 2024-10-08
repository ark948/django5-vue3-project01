from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.reverse import reverse, reverse_lazy
from api.serializers import TestPostSerializer
from rest_framework import status
from rest_framework.authentication import BasicAuthentication

# Create your views here.

class RootAPIView(APIView):
    def get(self, request):
        return Response({
            "admin": reverse("admin:index", request=request),
            'bookmarker': reverse("bookmarker:index", request=request),
            'accounts': reverse("accounts:index", request=request),
        })
    
class TestFrontendConnection(APIView):
    def get(self, request):
        return Response({
            "info": "You getting this?"
        })
    
class TestFrontendConnectionPost(GenericAPIView):
    serializer_class = TestPostSerializer
    
    def post(self, request):
        s = self.serializer_class(data=request.data, context={'request': request})
        if s.is_valid(raise_exception=True):
            valid_data = s.validated_data
            if valid_data['message'] == 'hidden message':
                return Response({
                    "Answer": "Hidden message is correct, Thank You."
                }, status=status.HTTP_200_OK)
        return Response({"Answer": "Wrong answer"}, status=status.HTTP_200_OK)
    

