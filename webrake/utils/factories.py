from .utils import add_attribute

def make_get_has_header_methods_for_obj_with_response(cls):
	""" 
	Dynamically create methods for the headers in a response object, 
	and append those methods to a class (not the instance).
	"""

	if not hasattr(cls, 'response'):
		raise AttributeError('The instance of %r has no attribute `response`' % cls) 
	elif not hasattr(cls.response, 'headers'): 
		raise AttributeError('%r instance\'s `response` attribute has no attribute `headers`' % cls) 

	#### Methods Wrapper ##############################
	def _make_method(header_name, create_has_method=True):
		""" Create a method for a header """			
		#### Methods to make #################
		def _has_header(self):
			""" Return Flase if header value is None """
			if header_name not in self.response.headers:
				self.response.headers[header_name] = None
			return self.response.headers[header_name] != None

		def _get_header(self): 
			""" Returns the header value """
			if header_name not in self.response.headers:
				self.response.headers[header_name] = None
			return self.response.headers[header_name]
		######################################
	
		# Create a valid function name
		func_name = header_name
		for INVALID in ('-', ' '):
			func_name = func_name.replace(INVALID, '_')

		if create_has_method:
			_method = _has_header
			_method.__name__ = 'has_%s_header' %  func_name
		else:
			_method = _get_header
			_method.__name__ = 'get_%s_header' % func_name
		return _method
	###################################################


	for header_name in self.response.headers:
		_has_method = _make_method(header_name, create_has_method=True)
		_get_method = _make_method(header_name, create_has_method=False)
		setattr(HistoryEntry, _has_method.__name__, _has_method)
		setattr(HistoryEntry, _get_method.__name__, _get_method)
