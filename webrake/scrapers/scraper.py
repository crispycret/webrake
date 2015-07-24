import time
import datetime

import requests
from bs4 import BeautifulSoup as BS

from ..parser import ParsingManager
from ..parser.handles import Page_Info_Handle

from ..utils import is_type_of, is_
from ..utils.urls import LazyUrl
from ..utils.history import HistoryEntry, HistoryManager




class BaseScraper(HistoryManager):
	""" 
	A handle to communicate with web servers. 
	HistoryManager: Collects requests/responses.
	"""

	def __init__(self, url, name='BaseScraper'):
		super(BaseScraper, self).__init__()
		self.name = name
		self.url = LazyUrl(url)
		self.response = requests.Response()

	def __repr__(self):
		return '<%s: %s>' % (self.__class__.__name__, self.name)

	### HistoryManager Method Overrides ###
	def create_history_entry(self):
		super(BaseScraper, self).create_history_entry(self.url, self.response)

	### Request Methods ###
	def get(self, payload={}):
		self.response = requests.get(self.url, params=payload)
		self.create_history_entry()

	def post(self, payload={}):
		self.response = requests.post(self.url, params=payload)
		self.create_history_entry()

	# Functionalites
	def return_soup(self):
		""" Returns a BeautifulSoup object """
		is_type_of(requests.Response, self.response)
		return BS(self.response.text, 'html5lib')

	def sleep(seconds=5):
		time.sleep(seconds)

	### File Maanipulations
	def save_file(self, relpath='.', image_name=None, host_as_dir=True):
		"""
		Save a file that being hosted over the web such as html, pdf, images, etc.
		relpath - The relative path of the current direcotry 
		host_as_dir - use the hostname to create a folder where the image will be stored.
		EXAMPLE: 
		http://www.joomlaworks.net/images/demos/galleries/abstract/7.jpg
		/path/to/current/directory/relative_path/www.joomlaworks.net/images_demos_galleries_abstract_7.jpg
		"""
		current_path = os.getcwd()
		current_path = os.path.join(current_path, relpath)

		if host_as_dir:
			dir_contents = os.listdir(current_path)
			current_path = os.path.join(current_path, self.url.host)

			# Create directory if missing
			if (self.url.host not in dir_contents): 
				os.mkdir(current_path)

			# If it's a file, replace it with a directory
			elif not os.path.isdir(current_path):
				os.remove(current_path)
				os.mkdir(current_path)

		if not image_name:
			image_name = self.url.path.replace('/', '_')

		final_path = os.path.join(current_path, image_name)
		image_handle = open(image_name, 'wb')
		image_handle.write(self.response.content)
		image_handle.close()


	### Load Html Files ###
	def load_html(self, html):
		""" Create a new Response object and stores the html in response.text. """
		self.response = requests.Response()
		self.response.html = html
		
	def load_html_file(self, path):
		""" Loads the source code of an html file into the response object """
		html = open(path, 'r').read()
		return self.load_html(html)







class Scraper(ParsingManager, BaseScraper):
	""" 
	A scraper also containing the functionality of the PageInfoHandle.

	PageInfoParsingHandle: 
	When a request is made this parser will gather common data like javascript/css/browser title, etc. 
	Any information that is constant across all html files.
	"""

	def __init__(self, url, name='Scraper'):
		super(Scraper, self).__init__(url, name)
		self.add_handle(Page_Info_Handle())

	def get_browser_title(self):
		return self.page_info_handle.title

	def get(self, payload={}):
		""" Preform a GET request """
		super(Scraper, self).get(payload)
		self.page_info_handle.set_soup(self.return_soup())
		self.page_info_handle.handle()

	def post(self, payload={}):
		""" Preform a POST a request """
		super(Scraper, self).post(payload)
		self.page_info_handle.set_soup(self.return_soup())
		self.page_info_handle.handle()

	def get_using_handle(self, handle, payload={}, raise_error=True):
		is_handle(handle)
		handle.has_url(raise_error)
		self,url = handle.url
		self.get(payload)
		return handle.handle

	def get_using_handle_by_name(self, handle_name, payload={}, raise_error=True):
		handle = self.get_handle(handle_name)
		return self.get_using_handle(handle, payload, raise_error)
