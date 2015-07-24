

""" Preset Handles """
	
class Page_Info_Handle(ParsingHandle):
	""" This Parsing Handle will grab common data from the soup object like the title """
	title = ''

	def handle(self):
		self.title = self.soup.title

