from bookmarker.models import Bookmark
from rest_framework import serializers
from rest_framework.serializers import (
    Serializer,
)

class BookmarksSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bookmark
        fields = ["id", "title", "url", "icon", "owner"]
        extra_keyworkds = {"id": { "write_only": True }}

class BookmarkDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        extra_keywords = {"owner": {"write_only": True}}