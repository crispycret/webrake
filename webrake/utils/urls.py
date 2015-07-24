import urlparse


### URL API ####################################################################
class LazyUrl(object):
	""" 
	A more friendly API to urls, using the urlparse library to split and join
	urls.
	"""
	### Variable Declaration ##################################
	ALLOWED_SCHEMES = ('http', 'https')
	scheme, host, path, params, query, fragment = ('','','','','','')
	###########################################################

	### Builtin Methods #######################################
	def __init__(self, url):
		self.set_url(url)	

	def __repr__(self): return '<LazyUrl: %s>' % self.url
	def __str__(self): return self.url
	def __unicode__(self): return unicode(self.url)
	def __iter__(self):
		for p in (self.scheme, self.host, self.path, 
		self.params, self.query, self.fragment,):
			yield p
	def __eq__(self, other):
		if other == self.url:
			return self.url == True
		if isinstance(other, self.__class__):
			return other.__dict__ == self.__dict__:
		return False
	def __ne__(self, other):
		return not self.__eq__(other)
	###########################################################

	### Modualarzed Methods ###################################
	#### urlparser Wrappers ############
	def join_url(self, join=True):
		""" Iterate over the url pieces and join them together. """
		if join:
			self.url = urlparse.urlunparse(self)
	####################################


	### Full Path Methods ##############
	def get_full_path(self):
		""" Return the url without the scheme and host parts """
		idx = len(self.scheme) + len(self.host) + 3 # +3 for ://
		return self.url[idx:]

	def clear_full_path(self):
		""" Remove all url pieces except the scheme and host """
		self.set_path('', False)
		self.set_params('', False)
		self.set_query('', False)
		self.set_fragment('', False)
	####################################


	### Set Methods ####################
	def set_url(self, url):
		""" Replace the url, check if it's valid, attempt a fix  """
		self.url = url
		self.parse_url()
		self.diagnose_fix_url()

	def set_scheme(self, scheme, join=True):
		""" Add/Replace the url scheme """
		self.scheme = scheme
		self.join_url(join)

	def set_host(self, host, join=True):
		""" Add/Replace the url host """
		self.host = host
		self.join_url(join)

	def set_path(self, path, join=True):
		""" Add/Replace the url path """
		if path[0] == '/': path = path[1:]
		self.path = path
		self.join_url(join)

	def set_params(self, params, join=True):
		""" Add/Replace the url params """
		self.params = params
		self.join_url(join)

	def set_query(self, query, join=True):
		""" Add/Replace the url query """
		self.query = query
		self.join_url(join)

	def set_fragment(self, fragment, join=True):
		""" Add/Replace the url fragment """
		self.fragment = fragment
		self.join_url(join)
	####################################
	###########################################################


	### Prope / Inspection Mehods #############################
	def print_overview(self, url=None):
		if isinstance(urlparse.ParseResult, url):
			url.host = url.netloc
			url.url = url.geturl()
		else:
			url = self
	
		print '\nOverview:\n'
		print '\tUrl: %s\n' % url.url
		print '\tScheme: %s' % url.scheme
		print '\tHost: %s' % url.host
		print '\tPath: %s' % url.path	
		print '\tQuery: %s' % url.query
		print '\tFragment: %s\n' % url.fragment
	###########################################################



	### Rule / Correction Methods #############################
	def diagnose_fix_url(self, output_results=False):
		""" Locate any bugs in the url, and attempt to fix them. """
		url = urlparse.urlparse(self.url)

		if url.scheme not in self.ALLOWED_SCHEMES:
			self.set_scheme(self.ALLOWED_SCHEMES[0], join=False)

		if url.netloc == '':
			# The host got placed in the path, with no path, move it
			if '/' not in url.path:
				self.set_host(url.path)
				self.set_path('')
			# The host got placed with path, seperate them
			else:
				path_pieces = url.path.split('/')
				path = '/'.join(path_pieces[2:])
				self.set_path(path, join=False)
				self.set_host(path_pieces[1], join=False)

		if output_results:
			self.print_overview(url)

		self.join_url()

	def parse_url(self):
		""" 
		Delegate the urlpieces from the returned urlpare.urlparse() method which is a urlparse.ParseResult()
		object. The reason being that the ParseResult() object inherits from collections.namedtuple() object
		that restricts access to attributes so that modification/set operations become impossible. 
		Also rename the ParseResult.netloc attribute to the more appropiate host attribute.
		"""
		parsed_url = urlparse.urlparse(self.url)

		self.scheme, self.host, self.path,\
		self.params, self.query, self.fragment = parsed_url
	###########################################################
################################################################################



