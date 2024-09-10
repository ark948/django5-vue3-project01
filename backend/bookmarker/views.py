from bookmarker.models import Bookmark
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from bookmarker.serializers import (
    BookmarkSerializer
)

# Create your views here.

class UserBookmarksList(generics.ListAPIView):

    serializer_class = BookmarkSerializer

    def get_queryset(self):
        user = self.request.user
        return Bookmark.objects.filter(owner=user.pk)

    def list(self, request):
        queryset = self.get_queryset()
        serializdr = BookmarkSerializer(queryset, many=True)
        return Response(serializdr.data)