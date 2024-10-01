from typing import Any
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm
)
from django.utils.translation import gettext_lazy as _
from django.core.validators import validate_email
from rest_framework.validators import ValidationError
from accounts.models import CustomUser
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class CripsyUserRegistrationForm(forms.Form):
    # crispy_forms
    email = forms.EmailField(label="Email:", max_length=120, required=True)
    first_name = forms.CharField(label="First Name:", max_length=50, required=True)
    last_name = forms.CharField(label="Last Name:", max_length=60, required=True)
    password = forms.CharField(label="Password:", max_length=120, required=True)
    confirm_password = forms.CharField(label="Repeat Password:", max_length=120, required=True)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'register-form'
        self.helper.form_class = 'form-class'
        self.helper.form_method = 'post'
        # reverse(html_register)
        self.helper.form_action = reverse('accounts:html_register')
        # submit button
        self.helper.add_input(Submit('submit', 'Submit'))
        self.helper.layout = Layout()
    

class BuiltinUserRegistrationForm(UserCreationForm):
    # cannot be used (CustomUser model has no username field), unless exclude is used
    # this works and password is hashed (OK)
    class Meta(UserCreationForm):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('email', )
        exclude = ['username']

class BuiltinUserChangeForm(UserChangeForm):
    # cannot be used (CustomUser model has no username field), unless exclude is used
    class Meta:
        model = CustomUser
        fields = UserChangeForm.Meta.fields
        exclude = ['username']

class CustomUserRegistrationForm(forms.ModelForm):
    email = forms.EmailField(max_length=200, required=True)
    password1 = forms.CharField(widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(widget=forms.PasswordInput, required=True)
    
    class Meta:
        model = get_user_model()
        fields = ['email', 'password1', 'password2']

    def email_clean(self):
        email = self.cleaned_data['email'].lower()
        new = CustomUser.objects.filter(email=email)
        if new.count():
            raise ValidationError("Email already exists.")
        return email
    
    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords do not match.")
        return password2

    def validate(self, value):
        for email in value:
            validate_email(email)

        if value['password1'] != value['password2']:
            raise ValidationError('Passwords do not match.')
        return value
        
    def save(self, commit=True) -> object:
        user = CustomUser.objects.create(email=self.cleaned_data['email'], first_name='', last_name='', password=self.cleaned_data['password1'])
        return user
    
class UserLoginForm(forms.Form):
    email = forms.CharField(required=True, max_length=200)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    
    def email_clean(self):
        email = self.cleaned_data['email'].lower()
        return email
    
    def validate(self, attr):
        for email in attr:
            validate_email(email)
        return attr
    
class VerifyAccountForm(forms.Form):
    otp = forms.IntegerField(min_value=100_000, max_value=999_999, required=True)


class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(required=True)

    def validate(self, attr):
        for email in attr:
            validate_email(email)
        return attr
    
class SetNewPasswordForm(forms.Form):
    password1 = forms.CharField(label='New Password:', widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(label='Repeat Password:', widget=forms.PasswordInput, required=True)

    def validate(self, attr):
        if attr.get('password1') != attr.get('password2'):
            raise ValidationError("Passwords do not match.")
        return attr
    
class UpdatePasswordForm(forms.Form):
    current_password = forms.CharField(label="Current Password:", widget=forms.PasswordInput, required=True)
    new_password = forms.CharField(label="New Password:", widget=forms.PasswordInput, required=True)
    repeat_password = forms.CharField(label="Repeat Password:", widget=forms.PasswordInput, required=True)

    def validate(self, attr):
        if attr.get('new_password') != attr.get('repeat_password'):
            raise ValidationError("New Passwords do not match.")
        return attr
