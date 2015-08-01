from collections import defaultdict 

from crispys_webkit import LazyUrl, get_class_name
from crispys_webkit import is_type_of, is_str, is_lazy_url, is_soup, has_soup
from crispys_webkit import add_attribute, validate_attribute_name



# Inherit from the data model when that class has been
# extrapolated on.
class ParsingHandle(object):
	""" 
	Structure of handle that is used to do one thing only, parse a soup object.
	Parsing of the soup object must take place in the handle method which must
	be defined explictly.
	"""
	name = None
	url = None
	soup = None

	def __init__(self, url='', soup=None):
		self.name = validate_attribute_name(get_class_name(self))
		if url: self.set_url(url)
		if soup: self.set_soup(soup)		

	def __repr__(self):
		return '<Handle: %s>' % self.name 

	def set_url(self, url):
		if is_lazy_url(url, ignore=True):
			self.url = url
		elif is_str(url):
			self.url = LazyUrl(url)

	def set_url_path(self, path):
		self.url.clear_full_path()
		self.url.set_path(path)
		
	def has_url(self, raise_error=False):
		has = False
		has = (self.url == True)
		if not has and raise_error:
			raise ValueError('%r is a false LazyUrl' % self.url)
		return has
	
	def set_soup(self, soup):
		""" Set the instance soup object to be used in handle """ 
		is_soup(soup)
		self.soup = soup

	def has_soup(self, raise_error=False):
		return has_soup(self, raise_error)

	def handle(self):
		""" Override with your own HTML parsing logic """
		pass # Do something with the soup object




def is_handle(handle):
	""" Call is_type_of() with ParsingHandle """ 
	is_type_of(handle, ParsingHandle)




class ParsingManager(list):
	""" 
	A list of ParsingHandles.
	The name of handles also become attributes for easy access. 
	"""
	def __init__(self):
		super(ParsingManager, self).__init__()

	def handle(self, handle, soup=None):
		if soup:
			is_soup(soup)
		elif handle.has_soup(raise_error=True):
			soup = handle.soup
		handle.set_soup(soup)
		return handle.handle()

	def handle_by_name(self, handle_name, soup=None):
		""" Invoke the handle method of the ParsingHandle with the handle_name """
		handle = self.get_handle(handle_name)
		return self.handle(handle, soup)

	def add_handle(self, handle):
		""" 
		Append only a new ParsingHandle to self, 
		which is a list and as an attribute of this instance (self)
		"""
		is_handle(handle) # integrity check
		self.does_handle_exist(handle.name, raise_error=True) # integrity check
		self.append(handle)
		add_attribute(self, handle.name, handle)
		

	def add_handles(self, *handles):
		""" 
		Add Many ParsingHandles, if new, to self, which is a list 
		and as an attribute of this instance (self)
		"""
		for handle in handles: 
			self.add_handle(handle)	

	def get_handle(self, handle_name, raise_error=True):
		""" return a ParsingHandle by it's name """
		handle = None
		for h in self:
			if h.name == handle_name:
				handle = h
		if not handle and raise_error:
			raise IndexError("Theres no ParsingHandle's with the name %s" % handle_name)
		return handle		

	def does_handle_exist(self, handle_name, raise_error=False):
		""" Returns a boolean of wether or not the ParsingHandle by it's name exists """ 
		found = False
		for handle in self:
			if handle.name == handle_name:
				found = True
				break
		if found and raise_error:
			raise ValueError("There is already a ParsingHandle with the name %s" % handle_name)
		return found



