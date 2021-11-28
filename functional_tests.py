from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest, time

class NewVisitorTest(unittest.TestCase):

	def setUp(self):
		self.browser = webdriver.Firefox()

	def tearDown(self):
		self.browser.quit()

	def test_build_list_and_retrieve_later(self):
		self.browser.get('http://localhost:8000')

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

		# enter "Buy peacock feathers" into textbox
		input_box.send_keys('Buy peacock feathers')
		input_box.send_keys(Keys.ENTER)
		time.sleep(1)

		# can view updated item
		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_elements_by_tag_name('tr')
		self.assertTrue(
			any( row.text == '1: Buy peacock feathers' for row in rows ),
			'New to-do item did not appear in table'
		)

		# enter "Make fly" into textbox from same page
		self.fail('Finish test!')

		# can see both items

		# closes & revists url to confirm to-do list exists

if __name__ == '__main__':
	unittest.main()
