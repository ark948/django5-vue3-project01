from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.reverse import reverse

# Create your views here.

class BookmarkerRootAPIView(APIView):
    def get(self, request):
        return Response({
            'api': reverse('bookmarker:api:list', request=request),
            'web': reverse('bookmarker:web:index', request=request)
        })