import unittest
from django.test import Client
from django.urls import reverse, resolve
from django.test import TestCase, RequestFactory
from accounts.models import CustomUser
from accounts.api.html_views import (
    HTMLIndexView,
    html_register_view,
    html_login_view,
    html_profile_page_view
)
from accounts.forms import (
    BuiltinUserRegistrationForm,
    UserLoginForm,
    UpdatePasswordForm,
    EditProfileForm,
    EmailChangeForm
)

# test urls (address and endpoint name)
# test views (response status code and which view)
# test templates
# test template context
# test corrcet form is aquired (if any)

class HTMLIndexViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.url = reverse('accounts:html_index')
        return super().setUpTestData()
    
    def setUp(self) -> None:
        self.client = Client()
        return super().setUp()
    
    def test_url_is_correct(self):
        response = self.client.get('/auth/html-index/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.url, '/auth/html-index/')

    def test_endpoint_is_correct(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_template_contains_accurate_text(self):
        response = self.client.get(self.url)
        self.assertContains(response, 'Welcome to index page')

    def test_view_is_the_correct_one(self):
        response = self.client.get(self.url)
        resolved = resolve(self.url)
        self.assertIs(response.resolver_match.func.view_class, HTMLIndexView)
        self.assertEqual(resolved.view_name, 'accounts:html_index')

    def test_app_name_is_correct(self):
        resolved = resolve('/auth/html-index/')
        self.assertEqual(resolved.app_name, 'accounts')


    def test_template_is_correct(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'accounts/index.html')
        self.assertTemplateNotUsed(response, 'accounts/login.html')


class HTMLRegisterViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.url = reverse("accounts:html_register")
        return super().setUpTestData()
    
    def setUp(self) -> None:
        self.client = Client()
        return super().setUp()
    
    def test_url_is_correct(self):
        response = self.client.get('/auth/html-register/')
        self.assertEqual(response.status_code, 200)

    def test_endpoint_is_correct(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_template_is_correct(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'accounts/register.html')
        self.assertTemplateNotUsed(response, 'accounts/index.html')
    
    def test_template_contains_accurate_text(self):
        response = self.client.get(self.url)
        self.assertContains(response, 'This is register page')

    def test_view_is_the_correct_one(self):
        response = self.client.get(self.url)
        self.assertIs(response.resolver_match.func, html_register_view)

    def test_app_name_is_accurate(self):
        resolved = resolve('/auth/html-register/')
        self.assertEqual(resolved.app_name, 'accounts')

    def test_correct_form_is_used(self):
        response = self.client.get(self.url)
        self.assertIsInstance(response.context['form'], BuiltinUserRegistrationForm)

    def test_user_registration(self):
        response = self.client.post(self.url, { 'email': 'testuser01@gmail.com', 'password1': 'home123*', 'password2': 'home123*'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.context['message'], 'success')
        
class HTMLLoginViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.url = reverse('accounts:html_login')
        cls.user = CustomUser.objects.create(email='testuser01@gmail.com')
        cls.user.set_password('home123*')
        cls.user.save()
        return super().setUpTestData()
    
    def setUp(self) -> None:
        self.client = Client()
        return super().setUp()
    
    def test_url_is_correct(self):
        response = self.client.get('/auth/html-login/')
        self.assertEqual(response.status_code, 200)

    def test_endpoint_is_valid(self):
        respnose = self.client.get(self.url)
        self.assertEqual(respnose.status_code, 200)

    def test_template_is_correct(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'accounts/login.html')
        self.assertTemplateNotUsed(response, 'accounts/register.html')

    def test_template_contains_accurate_text(self):
        response = self.client.get(self.url)
        self.assertContains(response, 'Login Page')

    def test_view_is_the_correct_one(self):
        response = self.client.get(self.url)
        self.assertIs(response.resolver_match.func, html_login_view)
        self.assertEqual(response.resolver_match.view_name, 'accounts:html_login')

    def test_app_name_is_accurate(self):
        resolved = resolve('/auth/html-login/')
        self.assertEqual(resolved.app_name, 'accounts')

    def test_correct_form_is_used(self):
        response = self.client.get(self.url)
        self.assertIsInstance(response.context['form'], UserLoginForm)

    def test_successful_user_login(self):
        response = self.client.post(self.url, { 'email': 'testuser01@gmail.com', 'password': 'home123*'})
        self.assertEqual(response.status_code, 302)

    def test_unsuccessful_user_login(self):
        response = self.client.post(self.url, { 'email': 'testuser01@gmail.com', 'password': 'home456*'})
        self.assertEqual(response.status_code, 401)

    @unittest.skip
    def test_view_is_inaccessible_to_logged_in_users(self):
        self.factory = RequestFactory()
        request = self.factory.get('/auth/html-login/')
        # setting user manually to simulate logged in user
        request.user = self.user
        response = html_login_view(request)
        self.assertEqual(response.status_code, 302)

    def test_view_is_inaccessible_to_logged_in_users02(self):
        self.client.post(self.url, {'email': 'testuser01@gmail.com', 'password': 'home123*'})
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_view_is_inaccessible_to_logged_in_users03(self):
        self.client.post(self.url, {'email': 'testuser01@gmail.com', 'password': 'home123*'})
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)


class HTMLProfilePageViewTestCase(TestCase):
    @classmethod
    @unittest.skip
    def setUpTestData(cls) -> None:
        cls.url = reverse('accounts:html_profile')
        cls.user = CustomUser.objects.create(email='testuser01@gmail.com')
        cls.user.set_password('home123*')
        cls.user.save()
        return super().setUpTestData()
    
    @unittest.skip
    def setUp(self) -> None:
        self.client = Client()
        self.client.post('/auth/html-login/', {'email': 'testuser01@gmail.com', 'password': 'home123*'})
        return super().setUp()
    
    @unittest.skip
    def test_url_is_correct(self):
        response = self.client.get('/auth/html-profile/')
        self.assertEqual(response.status_code, 200)

    @unittest.skip
    def test_endpoint_is_correct(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    @unittest.skip
    def test_template_is_correct(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'accounts/profile.html')
        self.assertTemplateNotUsed(response, 'accounts/login.html')

    @unittest.skip
    def test_template_contains_accurate_text(self):
        response = self.client.get(self.url)
        self.assertContains(response, 'Your profile page')

    @unittest.skip
    def test_view_is_the_correct_one(self):
        response = self.client.get(self.url)
        self.assertIs(response.resolver_match.func, html_profile_page_view)
        self.assertEqual(response.resolver_match.view_name, 'accounts:html_profile')

    @unittest.skip
    def test_app_name_is_accurate(self):
        resolved = resolve('/auth/html-profile/')
        self.assertEqual(resolved.app_name, 'accounts')

    @unittest.skip
    def test_correct_form_is_used(self):
        response = self.client.get(self.url)
        self.assertIsInstance(response.context['form1'], UpdatePasswordForm)
        self.assertIsInstance(response.context['form2'], EditProfileForm)
        self.assertIsInstance(response.context['form3'], EmailChangeForm)

    @unittest.skip
    def test_view_is_not_accessible_without_login(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)