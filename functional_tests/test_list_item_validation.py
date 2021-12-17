from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest

class ItemValidationTest(FunctionalTest):

	def test_cannot_add_empty_list_items(self):
		# home page submit blank
		self.browser.get(self.live_server_url)
		self.enter_todo_in_textbox('')

		# home page refresh with warning
		self.wait_for(lambda: self.assertEqual(
			self.browser.find_element_by_css_selector('.has-error').text,
			"You can't have an empty list item"
		))

		# enters first item correctly
		self.enter_todo_in_textbox('first item')
		self.wait_for_row_in_list_table('1: first item')

		# second blank item on list page
		self.enter_todo_in_textbox('')

		# list page refresh with warning
		self.wait_for(lambda: self.assertEqual(
			self.browser.find_element_by_css_selector('.has-error').text,
			"You can't have an empty list item"
		))

		# enters second item correctly
		self.enter_todo_in_textbox('second item')
		self.wait_for_row_in_list_table('2: second item')

		# fills it in correctly
		self.enter_todo_in_textbox('second item')
		self.wait_for_row_in_list_table('1: first item')
		self.wait_for_row_in_list_table('2: second item')


