from bookmarker.models import Bookmark, Category
from rest_framework.serializers import ModelSerializer, Serializer, FileField
from rest_framework import serializers


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class BookmarksSerializer(ModelSerializer):
    category_id = serializers.IntegerField(required=False, min_value=0, max_value=3)
    
    class Meta:
        model = Bookmark
        fields = ["id", "title", "url", "category_id", "icon"]
        extra_keyworkds = { "id": { "read_only": True } }

    def create(self, validated_data):
        user = self.context['request'].user
        if validated_data.get('category_id') == 0 or validated_data.get('category_id') == None:
            bookmark_item = Bookmark.objects.create(
            title=validated_data['title'],
            url = validated_data.get('url'),
            icon = validated_data.get('icon'),
            owner = user)
            return bookmark_item
        bookmark_item = Bookmark.objects.create(
        title=validated_data['title'],
        url = validated_data.get('url'),
        icon = validated_data.get('icon'),
        category_id = validated_data.get('category_id'),
        owner = user)
        return bookmark_item
        

class BookmarkDetailsSerializer(ModelSerializer):
    category_id = serializers.IntegerField(required=False, min_value=1, max_value=3)
    class Meta:
        model = Bookmark
        fields = ["title", "url", "icon", "category_id"]

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.url = validated_data.get('url', instance.url)
        instance.icon = validated_data.get('icon', instance.icon)
        instance.category_id = validated_data.get('category_id', instance.category_id)
        instance.save()
        return super().update(instance, validated_data)


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