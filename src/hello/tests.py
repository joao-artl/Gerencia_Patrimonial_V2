from django.test import TestCase
from django.urls import reverse

class HelloViewTest(TestCase):
    def test_hello_view_returns_200(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_hello_view_returns_expected_content(self):
        response = self.client.get('/')
        self.assertContains(response, "Hello, World!")
