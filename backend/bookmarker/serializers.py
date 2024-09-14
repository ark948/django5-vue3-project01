from bookmarker.models import Bookmark
from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import (
    Serializer,
)

class BookmarksSerializer(ModelSerializer):

    class Meta:
        model = Bookmark
        fields = ["id", "title", "url", "icon"]
        extra_keyworkds = { "id": { "read_only": True } }

    def create(self, validated_data):
        user = self.context['request'].user
        bookmark_item = Bookmark.objects.create(
            title=validated_data['title'],
            url = validated_data.get('url'),
            icon = validated_data.get('icon'),
            owner = user
        )
        return bookmark_item
        

class BookmarkDetailsSerializer(ModelSerializer):

    class Meta:
        model = Bookmark
        fields = ["title", "url", "icon"]