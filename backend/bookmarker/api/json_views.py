# django imports
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

# rest_framework imports
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework import status, viewsets
from rest_framework.request import Request
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.generics import (
    RetrieveUpdateDestroyAPIView,
    ListCreateAPIView,
    GenericAPIView,
    ListAPIView
    )

# local imports
from bookmarker.permissions import IsOwner
from bookmarker.models import Bookmark, Category
from bookmarker.api.serializers import (
    BookmarksSerializer, 
    BookmarkDetailsSerializer,
    BookmarkMultipleDeleteSerializer,
    FileUploadSerializer,
    CategorySerializer,
    BookmarksByCategorySerializer,
    BookmarksWithCategory
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
    
import csv
# import codecs
import io
class UserBookmarksCSVImport(APIView):
    parser_classes = (FormParser, MultiPartParser)
    seralizer_class = FileUploadSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.seralizer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            uploaded_file = serializer.validated_data['uploaded_file']
            f = uploaded_file.read().decode('utf-8-sig')
            csv_reader = csv.DictReader(io.StringIO(f))
            for line in csv_reader:
                Bookmark.objects.create(title=line['Title'], url=line['URL'], owner=self.request.user)
                print("ITEM ADDED.")
            return Response({'msg': 'csv file successfully imported.'}, status=status.HTTP_200_OK)
        return Response({'msg': "Not valid"}, status=status.HTTP_400_BAD_REQUEST)


# PROBLEM
@login_required
@api_view(['GET'])
def get_categories_with_link_ERROR(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_categories(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# OK
# just get categories
class GetCategories(ListAPIView):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Category.objects.all()
    

# OK
class GetBookmarksByCategory(ListAPIView):
    serializer_class = BookmarksByCategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # return Category.objects.filter(bookmarks__owner_id=user.pk)
        # prefetch_related is used to take care of performance issues of fetching nested database objects
        qs = Category.objects.prefetch_related('bookmarks')
        return qs



class GetBookmarksWithCategory(ListAPIView):
    serializer_class = BookmarksWithCategory
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Bookmark.objects.filter(owner=user)
    