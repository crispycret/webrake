<<<<<<< HEAD
from setuptools import setup, find_packages
=======
from setuptools import setup


>>>>>>> 1bf6fc50bc7ebce7bb89011fdf96608b9932ca15


setup(
	name='webrake',
<<<<<<< HEAD
	version='0.1.1.a.dev',
	description='Web scraping library.',
	author='crispycret',
	license='MIT',
	packages=find_packages()
#	packages=['webrake'],
	#zip_safe=False
=======
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
>>>>>>> 1bf6fc50bc7ebce7bb89011fdf96608b9932ca15
)



<<<<<<< HEAD
=======

>>>>>>> 1bf6fc50bc7ebce7bb89011fdf96608b9932ca15
