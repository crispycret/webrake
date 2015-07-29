import os
import time
import datetime

import requests
from bs4 import BeautifulSoup as BS

from parser import ParsingManager, is_handle

from handles import Page_Info_Handle
from history import HistoryEntry, HistoryManager

from utils import is_type_of, is_soup, is_response
from utils import LazyUrl, is_lazy_url, get_class_name




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
		return '<%s: %s>' % (get_class_name(self), self.name)

	### Request Methods ########################################
	def get(self, payload={}):
		self.response = requests.get(self.url.url, params=payload)
		self.create_history_entry()

	def post(self, payload={}):
		self.response = requests.post(self.url.url, params=payload)
		self.create_history_entry()
	############################################################

	### HistoryManager Method Overrides ########################
	def create_history_entry(self):
		super(BaseScraper, self).create_history_entry(self.url, self.response)
	############################################################

	### Functionalites #########################################
	def set_url(self, url):
		if is_lazy_url(url, ignore=True):
			self.url = url
		else:
			self.url = LazyUrl(url)
	def get_soup(self):
		""" Returns a BeautifulSoup object """
		if_response(self.response)
		return BS(self.response.text, 'html5lib')

	def sleep(seconds=5):
		time.sleep(seconds)

	###### File Manipulations #########################
	def load_html(self, html):
		""" Create a new Response object and stores the html in response.text. """
		self.response = requests.Response()
		self.response.html = html
		
	def load_html_file(self, path):
		""" Loads the source code of an html file into the response object """
		html = open(path, 'r').read()
		return self.load_html(html)

	def save_file(self, relpath='.', file_name=None, host_as_dir=True):
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

		if not file_name:
			file_name = self.url.path.replace('/', '_')
			if file_name in ('_', ''):
				file_name = 'home'

		final_path = os.path.join(current_path, file_name)
		file_handle = open(file_name, 'wb')
		file_handle.write(self.response.content)
		file_handle.close()
	###################################################
	############################################################





class PageInfoMixin(object):
	""" Methods to acquire data from the Page_Info_Handle() """ 

	### Get Methods ############################################
	def get_browser_title(self):
		return self.handles.page_info_handle.title
	############################################################

	### Extract Methods ########################################
	def _extract_page_info(self):
		self.handles.page_info_handle.set_soup(self.get_soup())
		self.handles.page_info_handle.handle()
	############################################################

	### Include Methods ########################################
	def _include_page_info_handle(self):
		self.add_handle(Page_Info_Handle())
	############################################################

	## Scraper Override Methods ################################
	def get(self, *args, **kwargs):
		super(PageInfoMixin, self).get(*args, **kwargs)
		self._extract_page_info()
	
	def post(self, *args, **kwargs):
		super(PageInfoMixin, self).post(*args, **kwargs)
		self._extract_page_info()
	############################################################





class ParsingManageShortcutsrMixin(object):
	""" 
	A class that allows access to handle methods for the scraper
	without referencing the ParsingManager itself.
	"""
	### Shortcut Wrapper Methods ###############################
	def add_handle(self, handle):
		self.handles.add_handle(handle)
	def add_handles(self, *handles):
		self.handles.add_handles(*handles)
	def handle(self, handle, soup=None):
		self.handles.handle(handle, soup)
	def handle_by_name(self, handle_name, soup=None):
		self.handles.handle_by_name(handle_name, soup)
	def get_handle(self, handle_name, raise_error=True):
		self.handles.get_handle(handle_name, raise_error)
	############################################################






class Scraper(
	ParsingManageShortcutsrMixin, 
	PageInfoMixin,
	BaseScraper
):
	""" 
	A more advanced scraper that has ParsingManager.
	"""

	def __init__(self, url, name='Scraper'):
		super(Scraper, self).__init__(url, name)
		self.handles = ParsingManager()
		self._mixin_inits()		

		print self.handles

	def _mixin_inits(self):
		self._include_page_info_handle()

	### Normal Request Methods #################################
	def get(self, payload={}):
		""" Preform a GET request """
		super(Scraper, self).get(payload)

	def post(self, payload={}):
		""" Preform a POST a request """
		super(Scraper, self).post(payload)
	############################################################


	### Common Functionalities #################################
	def get_using_handle(self, handle, payload={}, raise_error=True):
		is_handle(handle) # integrity check
		handle.has_url(raise_error) # integrity check
		self.url = handle.url
		self.get(payload)
		hanle.set_soup(self.get_soup())
		return handle.handle()

	def get_using_handle_by_name(self, handle_name, payload={}, raise_error=True):
		handle = self.handles.get_handle(handle_name)
		return self.get_using_handle(handle, payload, raise_error)
	############################################################


