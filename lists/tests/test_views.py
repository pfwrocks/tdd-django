from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.utils.html import escape
from lists.views import home_page
from lists.models import Item, List

class HomePageTest(TestCase):
	def test_uses_home_page_template(self):
		response = self.client.get('/')
		self.assertTemplateUsed(response, 'home.html')

class ListViewTest(TestCase):
	def test_uses_list_template(self):
		lst = List.objects.create()
		response = self.client.get(f'/lists/{lst.id}/')
		self.assertTemplateUsed(response, 'list.html')

	def test_displays_only_items_for_that_list(self):
		correct_list = List.objects.create()
		Item.objects.create(text='I1', list=correct_list)
		Item.objects.create(text='I2', list=correct_list)
		wrong_list = List.objects.create()
		Item.objects.create(text='I3', list=wrong_list)
		Item.objects.create(text='I4', list=wrong_list)

		response = self.client.get(f'/lists/{correct_list.id}/')

		self.assertContains(response, 'I1')
		self.assertContains(response, 'I2')
		self.assertNotContains(response, 'I3')
		self.assertNotContains(response, 'I4')

	def test_passes_correct_list_to_template(self):
		correct_list = List.objects.create()
		wrong_list = List.objects.create()
		response = self.client.get(f'/lists/{correct_list.id}/')
		self.assertEqual(response.context['list'], correct_list)

	def test_can_save_POST_request_to_existing_list(self):
		right_list = List.objects.create()
		wrong_list = List.objects.create()

		self.client.post(
			f'/lists/{right_list.id}/',
			data={'item_text': 'I1'}
		)

		self.assertEqual(Item.objects.count(), 1)
		new_item = Item.objects.first()
		self.assertEqual(new_item.text, 'I1')
		self.assertEqual(right_list, new_item.list)

	def test_POST_redirects_to_list_view(self):
		right_list = List.objects.create()
		wrong_list = List.objects.create()
		response = self.client.post(
			f'/lists/{right_list.id}/',
			data={'item_text': 'I1'}
		)
		self.assertRedirects(response, f'/lists/{right_list.id}/')

	def test_validation_errors_end_up_on_lists_page(self):
		list_ = List.objects.create()
		response = self.client.post(
		    f'/lists/{list_.id}/',
		    data={'item_text': ''}
		)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'list.html')
		expected_error = escape("You can't have an empty list item")
		self.assertContains(response, expected_error)

class NewListTest(TestCase):
	def test_can_save_POST_request(self):
		response = self.client.post('/lists/new', data={'item_text': 'test list item'})
		self.assertEqual(Item.objects.count(), 1)
		self.assertEqual(Item.objects.first().text, 'test list item')

	def test_redirects_after_POST_request(self):
		response = self.client.post('/lists/new', data={'item_text': 'test list item'})
		lst = List.objects.first()
		self.assertRedirects(response, f'/lists/{lst.id}/')

	def test_validation_errors_sent_back_to_home_page_template(self):
		response = self.client.post('/lists/new', data={'item_text': ''})
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'home.html')
		expected_error = escape("You can't have an empty list item")
		self.assertContains(response, expected_error)
	
	def test_invalid_list_items_arent_saved(self):
		self.client.post('/lists/new', data={'item_text': ''})
		self.assertEqual(List.objects.count(), 0)
		self.assertEqual(Item.objects.count(), 0)
