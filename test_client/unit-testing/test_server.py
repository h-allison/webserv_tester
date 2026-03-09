import unittest
import calculator

class TestServer(unittest.TestCase):
	def test_get_requests(self): # read about self
		with open(basic_html, 'r') as file:
		resource_content = file.read()
		resource_lines = resource_content.splitlines()
		response = get.basic()
		self.assertEqual(get.basic(basic_html), 
