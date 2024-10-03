from bookmarker.models import Bookmark, Category
from rest_framework.serializers import ModelSerializer, Serializer, FileField
from rest_framework import serializers


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ('title', )


class BookmarksSerializer(ModelSerializer):
    class Meta:
        model = Bookmark
        fields = ["id", "title", "url", "category", "icon"]
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
    
class FileUploadSerializer(Serializer):
    uploaded_file = serializers.FileField()
    class Meta:
        fields = ['file_upload']


class BookmarkSerializer(ModelSerializer):
    class Meta:
        model = Bookmark
        fields = ['title', 'url', 'icon', 'category']


class BookmarksByCategorySerializer(ModelSerializer):
    bookmarks = BookmarkSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['title', 'bookmarks']


class BookmarksWithCategory(ModelSerializer):
    class Meta:
        model = Bookmark
        fields = '__all__'