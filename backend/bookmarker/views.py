from bookmarker.models import Bookmark
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from bookmarker.serializers import (
    BookmarksSerializer,
    BookmarkDetailsSerializer
)

# Create your views here.

class UserBookmarksList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BookmarksSerializer

    def get_queryset(self):
        user = self.request.user
        return Bookmark.objects.filter(owner=user.pk)

    def list(self, request):
        queryset = self.get_queryset()
        serializdr = BookmarksSerializer(queryset, many=True)
        return Response(serializdr.data)
    
class UserBookmarkDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BookmarkDetailsSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        object_id = self.request.attr.get('id')
        return Bookmark.objects.get(id=object_id)

    