from .thirdparty import BS


def is_type_of(cls, instance):
	""" raise a TypeError if builtin method`isinstance()` is False """
	if not isinstance(cls, instance):
		raise TypeError('%r does not inherit from %r' % (obj, cls))
	return True

def is_soup(soup):
	""" Call is_type_of() with BeautifulSoup """ 
	return is_type_of(BS, soup)

def is_or_has_soup(cls, soup=None):
	""" 
	If soup is None and cls has a soup object, delegate the instances soup
	object, proceed to check if soup a BeautifulSoup object by calling is_soup.
	Return the soup.
	"""
	if not soup and hasattr(cls, 'soup'): 
		soup = cls.soup
	is_soup(soup)
	return soup
