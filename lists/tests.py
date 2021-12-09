from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from lists.views import home_page
from lists.models import Item, List

class HomePageTest(TestCase):
	def test_uses_home_page_template(self):
		response = self.client.get('/')
		self.assertTemplateUsed(response, 'home.html')

class ListAndItemModelsTest(TestCase):
	def test_saving_and_retreiving_items(self):
		lst = List()
		lst.save()

		first_item = Item()
		first_item.text = 'first test item'
		first_item.list = lst
		first_item.save()

		second_item = Item()
		second_item.text = 'second test item'
		second_item.list = lst
		second_item.save()

		saved_list = List.objects.first()
		self.assertEqual(saved_list, lst)

		saved_items = Item.objects.all()
		self.assertEqual(saved_items.count(), 2)

		first_saved_item = saved_items[0]
		second_saved_item = saved_items[1]
		self.assertEqual('first test item', first_saved_item.text)
		self.assertEqual(first_saved_item.list, lst)
		self.assertEqual('second test item', second_saved_item.text)
		self.assertEqual(second_saved_item.list, lst)

class ListViewTest(TestCase):
	def test_uses_list_template(self):
		response = self.client.get('/lists/only-list/')
		self.assertTemplateUsed(response, 'list.html')

	def test_displays_all_items(self):
		lst = List.objects.create()
		Item.objects.create(text='I1', list=lst)
		Item.objects.create(text='I2', list=lst)

		response = self.client.get('/lists/only-list/')
		self.assertContains(response, 'I1')
		self.assertContains(response, 'I2')

class NewListTest(TestCase):
	def test_can_save_POST_request(self):
		response = self.client.post('/lists/new', data={'item_text': 'test list item'})
		self.assertEqual(Item.objects.count(), 1)
		self.assertEqual(Item.objects.first().text, 'test list item')

	def test_redirects_after_POST_request(self):
		response = self.client.post('/lists/new', data={'item_text': 'test list item'})
		self.assertRedirects(response, '/lists/only-list/')