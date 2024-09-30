# api views that will return html parsed responses

# register (ok)
# verify account
# login (ok)
# test authenticated view
# logout (ok)
# password reset request
# password reset confirm
# set new password

from django.urls import reverse
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from accounts.forms import (
    BuiltinUserRegistrationForm,
    CustomUserRegistrationForm,
    UserLoginForm
)

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
            new_user = form.save()
            return Response({'message': "success", "user_id": new_user.id}, template_name='accounts/register.html')
        else:
            print(f'\n{form.errors}\n')
            return Response({'message': "error"}, template_name='accounts/register.html')
    else:
        if request.user.is_authenticated:
            messages.warning(request, 'You have already logged in.')
            return redirect('accounts:html_index')
        form = BuiltinUserRegistrationForm()
        return Response({'form': form}, template_name='accounts/register.html')


# OK (redirect upon faiiled login requires polishing)
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
                return redirect(request.GET.get('next', '/auth/html-index/'))
            else:
                messages.warning(request, "Incorrect credentials.")
                return redirect(reverse('accounts:html_index'))
        else:
            print(f'\n{form.errors}\n')
            messages.error(request, "Please check the credentials.")
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
    

@login_required
@api_view(['GET'])
@renderer_classes([TemplateHTMLRenderer])
def html_profile_page_view(request):
    return Response(template_name='accounts/profile.html')
