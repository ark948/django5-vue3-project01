from django.test import Client
from django.urls import reverse, resolve
from django.test import TestCase
from accounts.api.html_views import (
    HTMLIndexView,
    html_register_view
)
from accounts.forms import (
    BuiltinUserRegistrationForm
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
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['message'], 'success')
        self.assertEqual(response.context['user_id'], 1)
        