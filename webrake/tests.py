import unittest
import requests

from scrapers import BaseScraper, Scraper
from parser import ParsingHandle
from utils import is_response


class BaseScraperTest(unittest.TestCase):

	def setUp(self):
		self.scraper = BaseScraper(url='http://stackoverflow.com/', name='StackOverflow')

	def tearDown(self):
		self.scraper = None

	def test_get_request(self):
		self.scraper.set_url('http://stackoverflow.com')
		self.scraper.get()
		self.assertEqual(self.scraper.response.status_code, 200)

	def test_download_stackoverflow_home_page(self):
		self.scraper.set_url('http://stackoverflow.com')
		self.scraper.get()
		# Make a history for downloads, perferably just extend the HistoryEntry class
		# make a method on BaseScaper to check if the file downloaded and where.
		# - this may require another class to handle saving, loading and tracing files
		# modify the save_file method so that the file is not saved in the package. 
		self.scraper.save_file()

		self.assertEqual(self.scraper.response.status_code, 200)



class ScraperTest(unittest.TestCase):

	def test_create_scraper(self):
		scraper = Scraper(url='http://stackoverflow.com/', name='StackOverflow')
		scraper.get()
		self.assertEqual(self.scraper.response.status_code, 200)



if __name__ == '__main__':
	unittest.main()

