import datetime
from collections import defaultdict

import requests

from utils import LazyUrl
from utils import is_type_of, is_lazy_url, is_response
from utils import make_get_has_header_methods_for_obj_with_response


class HistoryEntry(object):

	def __init__(self, url, response, timestamp=None):
		if not timestamp:
			timestamp = datetime.datetime.now()
		if not is_lazy_url(url, ignore=True):
			url = LazyUrl(url)
	
		is_response(response)

		self.url = url
		self.response = response
		self.timestamp = timestamp

		make_get_has_header_methods_for_obj_with_response(self)

	def __repr__(self): return '<HistoryEntry: %s>' % self.url
	def __str__(self): return self.__repr__()




def is_history_entry(obj, ignore=False):
	return is_type_of(obj, HistoryEntry, ignore)




""" Will Replace HistoryManager/ParsingManager with a pandas object when more profiecent """
class HistoryManager(defaultdict):
	""" A list registered defaultdict fo managing HistorEntry's """

	def __init__(self):
		super(HistoryManager, self).__init__(list)

	def __repr__(self):
		""" Ovveride defaultdict(list) repr to a custom repr """
		defaultdict_repr = super(HistoryManager, self).__rep__()
		dict_results = defaultdict_repr[26:-1]
		return '<HistoryManager: %s>' % dict_results


	def add_history_entry(self, entry):
		is_history_entry(entry)
		self[entry.url.host] += [entry]

	def add_history_entries(self, *entries):
		""" Add many HistoryEntrys """
		for entry in entries:
			self.add_history_entry(entry)

	def create_history_entry(self, url, response, timestamp=None):
		self.add_history_entry(HistoryEntry(url, response, timestamp))

	def count(self):
		""" Counts the total number of HistoryEntry's """
		return len([entry for entry in self.values()])

	def display_history(self):
		""" Print the history """
		for site_name, entries in self.items():
			print '\n%s:' % site_name
			
			for entry in entries:
				full_path = entry.url.get_full_path()
				print '\t-- %s' % full_path





