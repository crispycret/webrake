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



