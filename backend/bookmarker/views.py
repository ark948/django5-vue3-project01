from bookmarker.models import Bookmark
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from rest_framework.permissions import IsAuthenticated
from bookmarker.permissions import IsOwner
from rest_framework.generics import (
    ListAPIView,
    RetrieveUpdateDestroyAPIView
)
from bookmarker.serializers import (
    BookmarksSerializer,
    BookmarkDetailsSerializer
)

# Create your views here.

class UserBookmarksList(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BookmarksSerializer

    def get_queryset(self):
        user = self.request.user
        return Bookmark.objects.filter(owner=user.pk)

    def list(self, request):
        queryset = self.get_queryset()
        serializdr = BookmarksSerializer(queryset, many=True)
        return Response(serializdr.data)

class UserBookmarkDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = BookmarkDetailsSerializer
    permission_classes = (IsOwner, )

    def get_queryset(self):
        user = self.request.user
        return Bookmark.objects.filter(owner=user)