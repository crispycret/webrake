from webrake import Scraper, ParsingHandle


url = 'stackoverflow.com'

sto_scraper = Scraper(url)
sto_scraper.get()

print sto_scraper.title



