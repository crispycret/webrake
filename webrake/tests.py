import unittest
import requests

from urls import LazyUrl
from utils import LazyPath
from scrapers import BaseScraper




class LazyUrlTests(unittest.TestCase):

	def test_create(self):
		self.lazy_url = LazyUrl('http://mangapark.me')
		self.assertEqual(str(self.lazy_url), str('http://mangapark.me/'))

	def test_create_with_bad_scheme(self):
		self.lazy_url = LazyUrl('hppt://mangapark.me')
		self.assertEqual(str(self.lazy_url), str('http://mangapark.me/'))

	def test_create_with_no_scheme(self):
		self.lazy_url = LazyUrl('mangapark.me')
		self.assertEqual(str(self.lazy_url), str('http://mangapark.me/'))


class LazyUrlErrorTests(unittest.TestCase): 
	pass



class BaseScraperTests(unittest.TestCase):

	def setUp(self):
		self.scraper = BaseScraper()

	def test_set_url(self):
		self.scraper.set_url('httpq://mangapark.me')
		self.assertEqual(str(self.scraper.url), 'http://mangapark.me/')

	def test_get_request(self):
		self.scraper.set_url('httpq://mangapark.me')
		self.scraper.get()
		
	def test_save_html_file(self):
		self.scraper.set_url('http://mangapark.me')
		self.scraper.get()
		
		self.assertEqual(self.scraper.res_status_code(), 200)
		self.assertEqual(str(self.scraper.response.url), 'http://mangapark.me/')

		lazy_path = LazyPath(self.scraper.url)

		self.assertEqual(lazy_path.getfilename(), 'home.html')
		# self.assertEqual(str(self.scraper.file_history[-1]))



if __name__ == '__main__':
	unittest.main()


