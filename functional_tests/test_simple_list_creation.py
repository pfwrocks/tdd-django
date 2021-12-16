from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class NewVisitorTest(FunctionalTest):

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
