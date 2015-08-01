import datetime
import urlparse
import requests

from crispys_webkit import LazyUrl, LazyPath
from crispys_webkit import get_class_name
from crispys_webkit import is_str, is_lazy_url, is_response



class FileCabnetMixin(object):
	""" Can Open/Load, and Store/Save files """

	file_history = []


	def add_file_history(self, lazy_path, file_operation):
		""" file_operation can be either save or load """
		self.file_history.append((file_operation, lazy_path, datetime.datetime.now()))

	def save_file(self):
		lazy_path = LazyPath(self.url)
		lazy_path.save(self.response.text)




class LazyUrlMixin(object):
	def set_url(self, url):
		if is_lazy_url(url, ignore=True):
			self.url = url
		elif is_str(url, ignore=True):
			self.url = LazyUrl(url)
		else:
			raise TypeError('Cannot set the url with %r. Use a LazyUrl or a str' % type(url))


class ResponseMixin(object):
	def last_status_code(self):
		return self.response.status_code
	def last_method(self):
		return self.response.method
	def last_content_length(self):
		return self.response.headers['content-length']



class BaseScraper(
	FileCabnetMixin,
	ResponseMixin, 
	LazyUrlMixin, 
	object
):
	""" 
	A handle to communicate with web servers. 
	HistoryManager: Collects requests/responses.
	"""
	url = None
	name = None
	response = requests.Response()

	def __init__(self, url=None, name=None):
		self.url = url
		self.name = name
		if url: self.set_url(url)
		if not name: self.name = get_class_name(self)

	def __repr__(self):
		return '<Scraper: %s>' % self.name

	def get(self, payload={}):
		self.response = requests.get(self.url, payload)
	def post(self, payload={}):
		self.response = requests.payload(self.url, payload)


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


