import News_Scraper

newsScraper = News_Scraper.NewsScraper("KO")
print(newsScraper.retrieveNews())
newsScraper.printNewsItems()

newsScraper.appendToNewsItemsLog()