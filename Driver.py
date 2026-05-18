import News_Scraper

newsScraper = News_Scraper.NewsScraper("KAA")
print(newsScraper.retrieveNews())
newsScraper.printNewsItems()

newsScraper.appendToNewsItemsLog()