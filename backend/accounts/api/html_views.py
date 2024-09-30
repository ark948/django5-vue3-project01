# api views that will return html parsed responses

# register (ok)
# verify account (ok)
# login (ok)
# test authenticated view - profile (ok)
# logout (ok)
# password reset request
# password reset confirm
# set new password

from rest_framework import status
from django.http import HttpRequest
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib import messages
from accounts.utils.email import send_code_to_user
from accounts.models import OneTimePassword
from django.contrib.auth.decorators import login_required
from accounts.forms import (
    BuiltinUserRegistrationForm,
    UserLoginForm,
    VerifyAccountForm
)

class HTMLIndexView(GenericAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    
    def get(self, request: HttpRequest, *args, **kwargs) -> Response:
        if request.accepted_renderer.format == 'html':
            return Response(template_name='accounts/index.html', status=status.HTTP_200_OK)
        
# OK
@api_view(['GET', 'POST'])
@renderer_classes([TemplateHTMLRenderer])
def html_register_view(request) -> Response:
    if request.method == 'POST':
        form = BuiltinUserRegistrationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            send_code_to_user(new_user.email)
            messages.success(request, "Registration successful. Check your email.")
            return Response({'message': "success"}, template_name='accounts/register.html', 
            status=status.HTTP_201_CREATED)
        else:
            print(f'\n{form.errors}\n')
            return Response({'message': "error"}, template_name='accounts/register.html', 
            status=status.HTTP_400_BAD_REQUEST)
    else:
        if request.user.is_authenticated:
            messages.warning(request, 'You have already registered.')
            return redirect('accounts:html_index')
        form = BuiltinUserRegistrationForm()
        return Response({'form': form}, template_name='accounts/register.html', status=status.HTTP_200_OK)


# OK (redirect upon faiiled login requires polishing)
@api_view(['GET', 'POST'])
@renderer_classes([TemplateHTMLRenderer])
def html_login_view(request) -> Response:
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user != None:
                login(request, user)
                messages.success(request, "Login successful. Welcome")
                return redirect(request.GET.get('next', '/auth/html-index/'))
            else:
                messages.warning(request, "Invalid credentials.")
                return Response({'message': "failure"}, template_name='accounts/login.html', 
                status=status.HTTP_401_UNAUTHORIZED)
        else:
            print(f'\n{form.errors}\n')
            messages.error(request, "Please check the credentials.")
            return Response({'message': "failure"}, template_name='accounts/login.html',
            status=status.HTTP_401_UNAUTHORIZED)
    else:
        if request.user.is_authenticated:
            messages.warning(request, "You have already logged in.")
            return redirect('accounts:html_index')
        form = UserLoginForm()
        return Response({'form': form}, template_name='accounts/login.html', status=status.HTTP_200_OK)
    

# OK
@api_view(['GET', 'POST'])
@renderer_classes([TemplateHTMLRenderer])
def html_logout_view(request) -> Response:
    if request.method == 'POST':
        logout(request)
        messages.success(request, "Logout successful.")
        return redirect('accounts:html_index')
    

# OK
@login_required
@api_view(['GET'])
@renderer_classes([TemplateHTMLRenderer])
def html_profile_page_view(request) -> Response:
    return Response(template_name='accounts/profile.html', status=status.HTTP_200_OK)


# OK
@login_required
@api_view(['GET', 'POST'])
@renderer_classes([TemplateHTMLRenderer])
def html_verify_account(request) -> Response:     
    if request.method == 'POST':
        form = VerifyAccountForm(data=request.POST)
        if form.is_valid():
            otpcode = form.cleaned_data['otp']
            try:
                user_code_obj = OneTimePassword.objects.get(code=otpcode)
                user = user_code_obj.user
                if not user.is_verified:
                    user.is_verified = True
                    user.save()
                    return Response({'message': "Verification successful. Thank you for signing up."}, 
                    status=status.HTTP_200_OK,
                    template_name='accounts/verify.html')
                return Response({'message': "Code is invalid or user is already verified."}, 
                status=status.HTTP_204_NO_CONTENT, template_name='accounts/verify.html')
            except OneTimePassword.DoesNotExist:
                return Response({'message': "Code was not found."}, status=status.HTTP_404_NOT_FOUND, template_name='accounts/verify.html')
        else:
            messages.error(request, 'Form is invalid.')
            return Response(status=status.HTTP_400_BAD_REQUEST, template_name='accounts/verify.html')
    else:
        if request.user.is_verified:
            messages.warning(request, "You have already verified your account.")
            return redirect('accounts:html_index')
        form = VerifyAccountForm()
        return Response({'form': form}, status=status.HTTP_200_OK, template_name='accounts/verify.html')
