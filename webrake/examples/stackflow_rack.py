""" Stack Overflow Web Scraper """

from ..scrapers import Scraper
from ..parser import ParsingHandle
from ..utils import is_soup, slugify




# First Method for creating a ParsingHandle and Scraper
class Home_Page_Handle(ParsingHandle):
	""" Scrape all the questions from the homepage """
	def __init__(self):
		"""
		Notice how the name paced is titled and has a space, it will be changed 
		to home_page. How this happens is the name is slugified then modified 
		so that dashes (-) become underscores (_).
		"""
		super(Home_Page_Handle, self).__init__('Home Page', '')

	def handle(self):
		# Scrape the question url, title, votes, answers, views
		# return a list of lists [url_path, title, votes, answers, views]
		pass


class Question_Author_Handle(ParsingHandle):
	""" Scrape the author from a question page """
	def __init__(self, url=''):
		super(Home_Page_Handle, self).__init__(name='Question Author', url=url)

	def handle(self):
		# Scrape the question author/poster
		# return the author's [url_path, name]
		pass


class User_Profile_Handle(ParsingHandle):
	""" scrape the users id, name, reputation, etc """
	def __init__(self):
		super(Home_Page_Handle, self).__init__(
			name='User, Profile', url='http://stackoverflow.com/users/')


	def set_url_path_with_attributes(self, user_id, user_name):
		if type(user_id) == str and not user_id.isdigit():
				raise ValueError('user_id is not an integer')
		user_id = int(user_id)
		user_name = slugify(user_name)

		path = '/users/%d/%s' % (user_id, user_name)
		self.set_url_path(path)


	def handle(self):
		# Just the id, name and rep for now
		pass




class StackOverflowScraper(Scraper):

	def __init__(self):
		super(StackOverflowScraper, self).__init__(self,
			url='http://stackoverflow.com',
			name='StackOverflow'
		)

		self.add_handle(Home_Page_Handle())
		self.add_handle(Question_Author_Handle())

	def scrape_question_info_and_poster_name(self):
		""" 
		Get available info of questions on the homepage, and get the posters 
		name and path to user profile. The latter requires a seperate request.
		"""
		questions = self.get_using_handle_by_name('home_page')

		# question = [url_path, title, votes, answers, views]
		for idx, question in enumerate(questions):
			self.url.clear_full_path()
			self.url.set_path(question[0])
			author_info = self.get_using_handle(self.question_author)
			questions[idx].append(author_info)
			self.sleep(3)

		# questions = [
		# 	[quesion_path, title, votes, answers, views, (user_path, username)],
		# 	[..], [..], [..], [..], [..], etc.
		# ]
		return questions

	def scrape_user_profiles_of_posters_on_homepage(self):
		questions = self.scrape_question_info_and_poster_name()
		# ...









# Second Method for creating a ParsingHandle and Scraper
def sto_user_profile_handle(self):
	""" Scrape info from a users profile """
	pass

handle = ParsingHandle('User_Profile', )
handle.handle = sto_user_profile_handle

STOScraper = Scraper('http://stackoverflow.com', 'StackOverflow')
STOScraper.add_handle(handle)

# STOScraper.get_using_handle(handle)
# or
# STOScraper.get_using_handle(STOScraper.user_profile)
# or
# STOScraper.get_using_handle('user_profile')




