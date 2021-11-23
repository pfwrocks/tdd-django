from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):

	def setUp(self):
		self.browser = webdriver.Firefox()

	def tearDown(self):
		self.browser.quit()

	def test_build_list_and_retrieve_later(self):
		self.browser.get('http://localhost:8000')

		self.assertIn('To-Do', self.browser.title)  
		self.fail('Finish the test!')

		# able to enter to-do

		# enter "Buy peacock feathers" into textbox

		# can view updated item

		# enter "Make fly" into textbox from same page

		# can see both items

		# closes & revists url to confirm to-do list exists

if __name__ == '__main__':
	unittest.main()
