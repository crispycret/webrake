from parser import ParsingHandle

""" Preset Handles """
	
class Page_Info_Handle(ParsingHandle):
	"""  
	When handle() is called this parser will gather common data like javascript/css/browser title, etc. 
	Any information that is constant across all html.
	"""
	title = ''
	scripts = []

	def handle(self):
		self.title = self.soup.title
		self.scripts = self.soup.findall('script')




Page_Info_Handle()