from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.reverse import reverse

# Create your views here.

class RootAPIView(APIView):
    def get(self, request):
        return Response({
            "auth": reverse("accounts:index", request=request),
        })