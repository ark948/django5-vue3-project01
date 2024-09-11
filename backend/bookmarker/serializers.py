from bookmarker.models import Bookmark
from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import (
    Serializer,
)

class BookmarksSerializer(ModelSerializer):

    class Meta:
        model = Bookmark
        fields = ["id", "title", "url", "icon", "owner"]
        extra_keyworkds = {"id": { "read_only": True }}

class BookmarkDetailsSerializer(ModelSerializer):

    class Meta:
        model = Bookmark
        fields = ["title", "url", "icon"]