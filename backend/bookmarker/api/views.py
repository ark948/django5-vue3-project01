from rest_framework.permissions import IsAuthenticated
from bookmarker.models import Bookmark
from rest_framework import viewsets
from rest_framework.response import Response
from bookmarker.permissions import IsOwner
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework import status
from rest_framework.request import Request
from django.shortcuts import get_object_or_404
from bookmarker.serializers import (
    BookmarksSerializer, 
    BookmarkDetailsSerializer,
    BookmarkMultipleDeleteSerializer
    )
from rest_framework.generics import (
    RetrieveUpdateDestroyAPIView,
    ListCreateAPIView,
    GenericAPIView
    )

# views

class BookmarkerHtmlRenderView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name='bookmarker/index.html'
    http_method_names = ['get']

    def get(self, request):
        return Response({})

class UserBookmarksListNoPagination(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BookmarksSerializer

    def get_queryset(self):
        user = self.request.user
        return Bookmark.objects.filter(owner=user.pk)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = BookmarksSerializer(queryset, many=True)
        return Response(serializer.data)
    
class UserBookmarksList(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BookmarksSerializer

    def get_queryset(self):
        user = self.request.user
        return Bookmark.objects.filter(owner=user.pk)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        serializer = BookmarksSerializer(page, many=True)
        return Response(serializer.data)


class UserBookmarkDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = BookmarkDetailsSerializer
    permission_classes = (IsOwner, )

    def get_queryset(self):
        user = self.request.user
        return Bookmark.objects.filter(owner=user)
    

class BookmarkViewSet(viewsets.ModelViewSet):
    serializer_class = BookmarksSerializer

    @action(methods=['DELETE'], detail=False)
    def delete(self, request: Request):
        delete_id = request.data
        delete_items = self.queryset.filter(id__in=delete_id)
        try:
            delete_items.delete()
            return Response(self.serializer_class(delete_items, many=True).data)
        except:
            print("multiple delete error")
            return Response({'msg': "error occurred."}, status=status.HTTP_400_BAD_REQUEST)


class BookmarksMultipleDelete(APIView):
    # unused, no url
    def get(self, request, pk_ids):
        ids = [int(pk) for pk in pk_ids.split(',')]
        BookmarkObject = Bookmark.objects.filter(id__in=ids)
        serializeBookmarkObject = BookmarksSerializer(BookmarkObject, many=True)
        return Response(serializeBookmarkObject.data)
    
    def delete(self, request, pk_ids):
        ids = [int(pk) for pk in pk_ids.split(',')]
        for i in ids:
            get_object_or_404(Bookmark, pk=i).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BookmarkMultipleDeleteUsingPost(GenericAPIView):
    serializer_class = BookmarkMultipleDeleteSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({}, status=status.HTTP_200_OK)
    
    def post(self, request, format=None):
        ids_list = request.data
        serializer = self.serializer_class(data=ids_list)
        if serializer.is_valid(raise_exception=True):
            for i in serializer.validated_data:
                try:
                    bookmark_object = Bookmark.objects.get(id=i)
                except Bookmark.DoesNotExist:
                    continue
                if bookmark_object.owner == self.request.user:
                    bookmark_object.delete()
            return Response({'msg': 'multiple records deleted.'}, status=status.HTTP_200_OK)
        return Response({'msg': 'data is not valid'})