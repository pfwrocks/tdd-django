from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import unittest, time

MAX_WAIT = 10

class NewVisitorTest(LiveServerTestCase):

	def setUp(self):
		self.browser = webdriver.Firefox()

	def tearDown(self):
		self.browser.quit()

	def wait_for_row_in_list_table(self, row_text):
		start_time = time.time()
		while True:
			try:
				table = self.browser.find_element_by_id('id_list_table')
				rows = self.browser.find_elements_by_tag_name('tr')
				self.assertIn(row_text, [row.text for row in rows])
				return
			except (AssertionError, WebDriverException) as e:
				if time.time()-start_time > MAX_WAIT:
					raise e
				time.sleep(0.1)

	def enter_todo_in_textbox(self, text):
		input_box = self.browser.find_element_by_id('id_new_item')
		input_box.send_keys(text)
		input_box.send_keys(Keys.ENTER)

	def test_start_list_for_single_user(self):
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
		self.wait_for_row_in_list_table('1: Buy peacock feathers')

		# enter "Make fly" into textbox from same page & can view both items
		self.enter_todo_in_textbox('Make fly')
		self.wait_for_row_in_list_table('1: Buy peacock feathers')
		self.wait_for_row_in_list_table('2: Make fly')

	def test_mutliple_users_can_build_lists_with_unique_urls(self):
		self.browser.get(self.live_server_url)
		
		# create to-do list
		self.enter_todo_in_textbox('Buy peacock feathers')
		self.wait_for_row_in_list_table('1: Buy peacock feathers')
		
		# check list exists at unique url
		user1_list_url = self.browser.current_url
		self.assertRegex(user1_list_url, '/lists/.+')

		## new browser session, so no cookie data remaining
		self.browser.quit()
		self.browser = webdriver.Firefox()

		# new user visits page, no evidence of previous list
		self.browser.get(self.live_server_url)
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Buy peacock feathers', page_text)
		self.assertNotIn('Make fly', page_text)

		# adds item
		self.enter_todo_in_textbox('Buy milk')
		self.wait_for_row_in_list_table('1: Buy milk')

		# gets unique url
		user2_list_url = self.browser.current_url
		self.assertRegex(user2_list_url, '/lists/.+')
		self.assertNotEqual(user1_list_url, user2_list_url)

		# only user2
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Buy peacock feathers', page_text)
		self.assertNotIn('Make fly', page_text)
		self.assertIn('Buy milk', page_text)

