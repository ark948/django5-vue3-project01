from django.test import Client
from django.urls import reverse, resolve
from django.test import TestCase
from accounts.api.html_views import (
    HTMLIndexView,
    html_register_view
)

# test urls (address and endpoint name)
# test views (response status code and which view)
# test templates
# test template context

class HTMLIndexViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        return super().setUpTestData()
    
    def setUp(self) -> None:
        self.client = Client()
        return super().setUp()
    
    def test_html_index_page_url(self) -> None:
        response = self.client.get('/auth/html-index/')
        url = reverse('accounts:html_index')
        resolved = resolve('/auth/html-index/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/index.html')
        self.assertContains(response, 'Welcome to index page')
        self.assertIs(response.resolver_match.func.view_class, HTMLIndexView)
        self.assertEqual(url, '/auth/html-index/')
        self.assertEqual(resolved.view_name, 'accounts:html_index')
        self.assertEqual(resolved.app_name, 'accounts')
        