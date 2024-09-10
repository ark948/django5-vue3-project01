from bookmarker.models import Bookmark
from rest_framework import serializers
from rest_framework.serializers import (
    Serializer,
)

class BookmarkSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bookmark
        fields = ["title", "url", "icon", "owner"]