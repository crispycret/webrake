from webrake.utils.utils import get_methods_of_class
from .scraper import Scraper



def test_stackoverflow():
	url = 'stackoverflow.com'
	s = Scraper(url, name='StackOverflow')

	s.get()

	# change: _make_get_has_header_methods()
	# to: _make_get_has_methods_for_headers()
	e = s['stackoverflow.com'][0]
	e._make_get_has_header_methods()

	methods = get_methods_of_class(HistoryEntry)
	method_names = [name for name, method in methods]
	print method_names, '\n\n'
	print e.get_content_length_header()

	print s.title.text




if __name__ == '__main__':
	test_stackoverflow()