# api views that will return html parsed responses

# register (ok)
# verify account (ok)
# login (ok)
# auth required - profile (ok)
# logout (ok)
# password reset request (ok)
# password reset confirm (ok)
# set new password (ok)
# change password (ok)
# edit profile (first and last name) (ok)
# edit email - requires re-verification (ok)

from django.urls import reverse
from rest_framework import status
from django.utils.encoding import smart_bytes, smart_str, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.http import HttpRequest
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from accounts.models import CustomUser
from django.contrib import messages
from accounts.utils.email import send_code_to_user, send_normal_email, re_verify_email
from accounts.models import OneTimePassword
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from accounts.forms import (
    BuiltinUserRegistrationForm,
    UserLoginForm,
    VerifyAccountForm,
    PasswordResetRequestForm,
    SetNewPasswordForm,
    UpdatePasswordForm,
    EditProfileForm,
    EmailChangeForm
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
            return redirect(reverse('accounts:html_index'))
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
            return redirect(reverse('accounts:html_index'))
        form = UserLoginForm()
        return Response({'form': form}, template_name='accounts/login.html', status=status.HTTP_200_OK)
    

# OK
@api_view(['GET', 'POST'])
@renderer_classes([TemplateHTMLRenderer])
def html_logout_view(request) -> Response:
    if request.method == 'POST':
        logout(request)
        messages.success(request, "Logout successful.")
        return redirect(reverse('accounts:html_index'))
    

# OK
# REMOVED url
@login_required
@api_view(['GET'])
@renderer_classes([TemplateHTMLRenderer])
def html_profile_page_view(request) -> Response:
    form1 = UpdatePasswordForm()
    form2 = EditProfileForm()
    form3 = EmailChangeForm()
    return Response({'form1': form1, 'form2': form2, 'form3': form3}, template_name='accounts/profile.html', status=status.HTTP_200_OK)


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
                    user_code_obj.delete()
                    # Delete verification code after successful use
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
            return redirect(reverse('accounts:html_index'))
        form = VerifyAccountForm()
        return Response({'form': form}, status=status.HTTP_200_OK, template_name='accounts/verify.html')
    
# OK
@api_view(['GET', 'POST'])
@renderer_classes([TemplateHTMLRenderer])
def html_password_reset_request(request):
    form = PasswordResetRequestForm()
    if request.method == 'POST':
        form = PasswordResetRequestForm(data=request.POST)
        if form.is_valid():
            user_email = form.cleaned_data['email']
            if CustomUser.objects.filter(email=user_email).exists():
                user = CustomUser.objects.get(email=user_email)
                uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
                token = PasswordResetTokenGenerator().make_token(user)
                site_domain = get_current_site(request).domain
                relative_link = reverse('accounts:html_password_reset_confirm', kwargs={'uidb64': uidb64, 'token': token})
                abslink = f'http://{site_domain}{relative_link}'
                email_body = f'Hi, Please use the following link to reset your password.\n {abslink}'
                data = {
                    'email_body': email_body,
                    'email_subject': "Reset your password.",
                    'to_email': user.email
                }
                send_normal_email(data)
                messages.success(request, "Reset link sent to your email.")
                return redirect(reverse('accounts:html_index'))
            else:
                return Response({'message': "Email was not found."}, template_name='accounts/reset_request.html')
    else:
        if request.user.is_authenticated:
            message = "You are logged in.\nIf you have lost your password, please logout and use the reset link."
            return Response({'message': message}, template_name='accounts/reset_request.html', status=status.HTTP_200_OK)
        else:
            return Response({'form': form}, template_name='accounts/reset_request.html', status=status.HTTP_200_OK)
    

# this has a huge problem
@api_view(['GET', 'POST'])
@renderer_classes([TemplateHTMLRenderer])
def html_password_reset_confirm(request, uidb64, token):
    if request.method == 'POST':
        pass
    else:
        if request.user.is_authenticated:
            return redirect(reverse('accounts:html_index'))
        try:
            # this will raise exception, neither will work
            uidb64 = request.params['uidb64'] or request.GET.get('uidb64')
        except Exception as error_getting_uridb64:
            print("ERROR")
        try:
            # this will raise exception, neither will work
            token = request.params['token'] or request.GET.get('token')
        except Exception as error_getting_token:
            print("ERROR2")
        print("uidb64", uidb64)
        print("token", token)
        user_id = force_str(urlsafe_base64_decode(uidb64))
        print('user_id --> ', user_id)
        user = CustomUser.objects.get(id=user_id)
        form = SetNewPasswordForm()
        if PasswordResetTokenGenerator().check_token(user, token):
            return Response({'uidb64': uidb64, 'token': token, 'form': form}, template_name='accounts/set_new_password.html')
        else:
            messages.error(request, "Link is invalid or expired.")
            return redirect(reverse('accounts:html_index'))
        

# OK
@api_view(['POST'])
@renderer_classes([TemplateHTMLRenderer])
def html_set_new_password(request):
    if request.method == 'POST':
        form = SetNewPasswordForm(data=request.POST)
        if form.is_valid():
            uidb64 = request.POST.get('uid')
            token = request.POST.get('tkn')
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
        else:
            messages.error(request, "Form was not valid.")
            return redirect(reverse('accounts:html_index'))
        user_id = force_str(urlsafe_base64_decode(uidb64))
        try:
            user = CustomUser.objects.get(id=user_id)
        except Exception as getting_user:
            messages.error(request, "User not found.")
            return redirect(reverse('accounts:html_index'))
        if PasswordResetTokenGenerator().check_token(user, token):
            if password1 == password2:
                user.set_password(password1)
                user.save()
                messages.success(request, "Password reset successful, login with new password.")
                return redirect(reverse('accounts:html_login'))
            else:
                messages.error(request, "Passwords do not match.")
                return redirect(reverse('accounts:html_index'))
        else:
            messages.error(request, "Token is invalid.")
            return redirect(reverse('accounts:html_index'))

# OK
@login_required
@api_view(['POST'])
@renderer_classes([TemplateHTMLRenderer])
def html_update_password(request):
    if request.method == 'POST':
        form = UpdatePasswordForm(data=request.POST)
        if form.is_valid():
            current_password = form.cleaned_data['current_password']
            new_password = form.cleaned_data['new_password']
            repeat_password = form.cleaned_data['repeat_password']
            user = CustomUser.objects.get(id=request.user.id)
            if user.check_password(current_password):
                if new_password == repeat_password:
                    user.set_password(new_password)
                    user.save()
                else:
                    messages.error(request, "Passwords do not match.")
                    return redirect(reverse('accounts:html_index'))
            else:
                messages.error(request, "Current password is incorrect.")
                return redirect(reverse('accounts:html_index'))
        else:
            messages.error(request, "Form was not valid.")
            return redirect(reverse('accounts:html_index'))
    return redirect(reverse('accounts:html_profile'))


# OK
# REMOVED url
@login_required
@api_view(['POST'])
@renderer_classes([TemplateHTMLRenderer])
def html_edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(data=request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            user = CustomUser.objects.get(id=request.user.id)
            if first_name:
                user.first_name = first_name
            else:
                pass
            if last_name:
                user.last_name = last_name
            else:
                pass
            user.save()
            messages.success(request, "Profile successfully updated.")
            return redirect(reverse('accounts:html_profile'))
        else:
            messages.success(request, "There was an error.")
            return redirect(reverse('accounts:html_profile'))
    return redirect(reverse('accounts:html_index'))


# OK
@login_required
@api_view(['POST'])
@renderer_classes([TemplateHTMLRenderer])
def html_change_email(request):
    if request.method == 'POST':
        form = EmailChangeForm(data=request.POST)
        if form.is_valid():
            new_email = form.cleaned_data['new_email']
            user = CustomUser.objects.get(id=request.user.id)
            if user.is_verified:
                user.email = new_email
                user.is_verified = False
                user.save()
                re_verify_email(user.id)
                messages.success(request, "Email changed successfully. Please check your email for verification link.")
            else:
                messages.error(request, "Your current email is not verified. You cannot change it.")
                return redirect(reverse('accounts:html_index'))
        else:
            messages.error(request, "Form is invalid.")
            return redirect(reverse('accounts:html_profile'))
    return redirect(reverse('accounts:html_profile'))