from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest, time

class NewVisitorTest(LiveServerTestCase):

	def setUp(self):
		self.browser = webdriver.Firefox()

	def tearDown(self):
		self.browser.quit()

	def check_row_in_list_table(self, row_text):
		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_elements_by_tag_name('tr')
		self.assertIn(row_text, [row.text for row in rows])

	def enter_todo_in_textbox(self, text):
		input_box = self.browser.find_element_by_id('id_new_item')
		input_box.send_keys(text)
		input_box.send_keys(Keys.ENTER)
		time.sleep(1)

	def test_build_list_and_retrieve_later(self):
		self.browser.get(self.live_server_url)

		# header and title mention To-Do
		self.assertIn('To-Do', self.browser.title)
		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertIn('To-Do', header_text)

		# able to enter to-do
		input_box = self.browser.find_element_by_id('id_new_item')
		self.assertEqual(
			input_box.get_attribute('placeholder'),
			'Enter a to-do item'
		)

		# enter "Buy peacock feathers" into textbox & can view item
		self.enter_todo_in_textbox('Buy peacock feathers')
		self.check_row_in_list_table('1: Buy peacock feathers')

		# enter "Make fly" into textbox from same page & can view both items
		self.enter_todo_in_textbox('Make fly')
		self.check_row_in_list_table('1: Buy peacock feathers')
		self.check_row_in_list_table('2: Make fly')

		self.fail('Finish Test!')

		# closes & revists url to confirm to-do list exists
