import unittest
import requests

from scrapers import BaseScraper

from crispys_webkit import LazyUrl, LazyPath



class LazyUrlTests(unittest.TestCase):

	def test_create(self):
		self.lazy_url = LazyUrl('http://stackoverflow.com/')
		self.assertEqual(str(self.lazy_url), str('http://stackoverflow.com/'))

	def test_create_with_bad_scheme(self):
		self.lazy_url = LazyUrl('gpsp://stackoverflow.com/')
		self.assertEqual(str(self.lazy_url), str('http://stackoverflow.com/'))

	def test_create_with_no_scheme(self):
		self.lazy_url = LazyUrl('stackoverflow.com')
		self.assertEqual(str(self.lazy_url), str('http://stackoverflow.com/'))


class LazyUrlErrorTests(unittest.TestCase): 
	pass



class BaseScraperTests(unittest.TestCase):

	def setUp(self):
		self.scraper = BaseScraper()

	def test_set_url(self):
		self.scraper.set_url('httpq://stackoverflow.com')
		self.assertEqual(str(self.scraper.url), 'http://stackoverflow.com/')

	def test_get_request(self):
		self.scraper.set_url('httpq://stackoverflow.com')
		self.scraper.get()
		
	def test_save_html_file(self):
		self.scraper.set_url('http://stackoverflow.com')
		self.scraper.get()
		
		self.assertEqual(self.scraper.last_status_code(), 200)
		self.assertEqual(str(self.scraper.response.url), 'http://stackoverflow.com/')

		lazy_path = LazyPath(self.scraper.url)

		# self.assertEqual(lazy_path.getfilename(), 'home.html')
		# self.assertEqual(str(self.scraper.file_history[-1]))





if __name__ == '__main__':
	unittest.main()

