from setuptools import setup




setup(
	name='webrake',
	version='0.1.0',
	
	author='Brandon Nadeau',
	author_email = 'brandonmnadeau@hotmail.com',
	
	packages=['webrake'],
	include_package_data=True,
	
	url = 'http://github.com/crispycret/webrake',
	
	license = 'MIT',
	# license='LICENSE.txt',
	
	description='Web Scraping Framework',
	# long_description = open('README.txt').read(),

	install_requires = [
		'requests',
		'beautifulsoup4',
		'crispys_webkit',
	],
	
	zip_safe = False
)




