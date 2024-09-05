from rest_framework.serializers import Serializer
from rest_framework import serializers

class TestPostSerializer(Serializer):
    message = serializers.CharField(min_length=1, max_length=64, required=True)