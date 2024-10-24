from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.reverse import reverse

# Create your views here.

class BookmarkerRootAPIView(APIView):
    def get(self, request):
        return Response({
            'list': reverse('bookmarker:list', request=request),
            'list-no-paginate': reverse('bookmarker:list_no_pagination', request=request),
            'categories': reverse('bookmarker:categories_list', request=request),
            'bookmarks-by-category': reverse('bookmarker:bookmarks_by_category', request=request),
            'bookmarks-with-category': reverse('bookmarker:bookmarks_with_category', request=request),
            'employees_index': reverse('bookmarker:emp_index', request=request),
            'employees_index_api': reverse('bookmarker:emp_index', request=request),
        })