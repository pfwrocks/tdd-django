from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from lists.views import home_page

class HomePageTest(TestCase):

	def test_uses_home_page_template(self):
		response = self.client.get('/')
		self.assertTemplateUsed(response, 'home.html')

	def test_can_save_POST_request(self):
		response = self.client.post('/', data={'item_text': 'test list item'})
		self.assertIn('test list item', response.content.decode())
		self.assertTemplateUsed(response, 'home.html')