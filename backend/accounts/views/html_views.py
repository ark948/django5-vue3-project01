# api views that will return html parsed responses

# register
# verify account
# login
# test authenticated view
# logout
# password reset request
# password reset confirm
# set new password


from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView

class HTMLUserRegisterView(GenericAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    
    def get(self, request, *args, **kwargs):
        if request.accepted_renderer.format == 'html':
            print("\nRequest was html\n")
            return Response(template_name='accounts/register.html')