from django.core.exceptions import ValidationError
from django.test import TestCase
from lists.models import Item, List

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

	def test_cannot_save_empty_list_item(self):
		lst = List.objects.create()
		item = Item(text='', list=lst)
		with self.assertRaises(ValidationError):
			item.save()
			item.full_clean()
