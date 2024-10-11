# django imports
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse


# rest_framework imports
from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


# local imports
from bookmarker.models import Category
from bookmarker.api.serializers import CategorySerializer
from bookmarker.decorators import user_is_employee


# not used
@user_passes_test(user_is_employee, login_url='/bookmarker', redirect_field_name=None)
@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated,))
@renderer_classes([TemplateHTMLRenderer, JSONRenderer])
def employees_index_test_view(request) -> Response:
    """
    index view for employees, returns both HTML or JSON representations
    """
    queryset = Category.objects.all()
    if request.accepted_renderer.format == 'html':
        data = {'categories': queryset}
        return Response(data, template_name='bookmarker/employees/index.html')

    if request.accepted_renderer.format == 'json':
        serializer = CategorySerializer(queryset, many=True)
        data = serializer.data
        return Response({"message": "Success"})



@api_view(['GET'])
@permission_classes([IsAuthenticated])
@renderer_classes([TemplateHTMLRenderer, JSONRenderer])
def emp_index(request):
    """
    index view for employees. (HTML, JSON)
    """
    if not request.user.groups.filter(name='Employees').exists():
        return Response({'message': "You are not an employee."})
    
    queryset = Category.objects.all()
    if request.accepted_renderer.format == 'html':
        return Response({'categories': queryset }, template_name='bookmarker/employees/index.html')

    # if request.accepted_renderer.format == 'json':
    serializer = CategorySerializer(queryset, many=True)
    data = serializer.data
    return Response(data, status=status.HTTP_200_OK)
