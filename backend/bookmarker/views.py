from bookmarker.models import Bookmark
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from rest_framework.permissions import IsAuthenticated
from bookmarker.permissions import IsOwner
from django.views.generic import TemplateView
from rest_framework.views import APIView
from rest_framework.reverse import reverse
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.generics import (
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
)
from bookmarker.serializers import (
    BookmarksSerializer,
    BookmarkDetailsSerializer
)

# Create your views here.

class BookmarkerRootAPIView(APIView):
    def get(self, request):
        return Response({
            "webview_html": reverse("bookmarker:webview_html", request=request),
            "webview_index": reverse("bookmarker:webview_index", request=request),
            "bookmarks list": reverse("bookmarker:get-list", request=request),
        })

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
    
class BookmarkerIndexView(TemplateView):
    template_name = "bookmarker/index.html"

class BookmarkerHtmlRenderView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name='bookmarker/index.html'
    http_method_names = ['get']

    def get(self, request):
        return Response({})