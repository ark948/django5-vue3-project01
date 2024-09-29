# api views that will return html parsed responses

# register (ok)
# verify account
# login (ok)
# test authenticated view
# logout (ok)
# password reset request
# password reset confirm
# set new password

from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from accounts.forms import (
    BuiltinUserRegistrationForm,
    CustomUserRegistrationForm,
    UserLoginForm
)
from accounts.managers import UserManager
from accounts.models import CustomUser
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect

class HTMLIndexView(GenericAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    
    def get(self, request, *args, **kwargs) -> Response:
        if request.accepted_renderer.format == 'html':
            return Response(template_name='accounts/index.html')
        
# OK
@api_view(['GET', 'POST'])
@renderer_classes([TemplateHTMLRenderer])
def html_register_view(request):
    if request.method == 'POST':
        form = BuiltinUserRegistrationForm(data=request.POST)
        if form.is_valid():
            print("for IS valid")
            new_user = form.save()
            print("form SAVED")
            return Response({'message': "success", "user_id": new_user.id}, template_name='accounts/register.html')
        else:
            print("form NOT valid")
            print(f'\n{form.errors}\n')
            return Response({'message': "error"}, template_name='accounts/register.html')
    form = BuiltinUserRegistrationForm()
    return Response({'form': form}, template_name='accounts/register.html')


# OK
@api_view(['GET', 'POST'])
@renderer_classes([TemplateHTMLRenderer])
def html_login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user != None:
                login(request, user)
                # return redirect(f"{settings.LOGIN_URL}?next={request.path}")
                return redirect('accounts:html_index')
        else:
            print(f'\n{form.errors}\n')
            return Response({'message': "failure"}, template_name='accounts/login.html')
    else:
        form = UserLoginForm()
        return Response({'form': form}, template_name='accounts/login.html')
    

# OK
@api_view(['GET', 'POST'])
@renderer_classes([TemplateHTMLRenderer])
def html_logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('accounts:html_index')