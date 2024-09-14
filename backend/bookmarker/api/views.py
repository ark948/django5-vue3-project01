from rest_framework.generics import (
    ListAPIView, 
    RetrieveUpdateDestroyAPIView,
    ListCreateAPIView
)
from rest_framework.permissions import IsAuthenticated
from bookmarker.serializers import BookmarksSerializer, BookmarkDetailsSerializer
from bookmarker.models import Bookmark
from rest_framework.response import Response
from bookmarker.permissions import IsOwner
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer

# views

class BookmarkerHtmlRenderView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name='bookmarker/index.html'
    http_method_names = ['get']

    def get(self, request):
        return Response({})

class UserBookmarksList(ListCreateAPIView):
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