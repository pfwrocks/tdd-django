from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest

class LayoutAndStylingTest(FunctionalTest):
	def test_layout_and_styling(self):
		# visit home page
		self.browser.get(self.live_server_url)
		self.browser.set_window_size(1024, 768)

		# styling in place
		input_box = self.browser.find_element_by_id('id_new_item')
		self.assertAlmostEqual(
			input_box.location['x'] + input_box.size['width'] / 2,
			512,
			delta=10
		)

		# begin new list
		self.enter_todo_in_textbox('I1')
		self.wait_for_row_in_list_table('1: I1')
		input_box = self.browser.find_element_by_id('id_new_item')
		self.assertAlmostEqual(
			input_box.location['x']+input_box.size['width']/2,
			512,
			delta=10
		)

