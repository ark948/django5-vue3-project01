from bookmarker.models import Bookmark
from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import Serializer
from rest_framework import serializers

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


class BookmarkMultipleDeleteSerializer(Serializer):
    list_of_ids = serializers.CharField(required=True)
    
    def validate(self, attrs):
        new_list = []
        my_list = attrs.get('list_of_ids').split(',')
        for i in my_list:
            try:
                int(i.strip())
            except ValueError:
                continue
            new_list.append(int(i.strip()))
        if len(new_list) == 0:
            raise serializers.ValidationError('Validation failed.')
        return new_list