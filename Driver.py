import News_Scraper
import Model

newsScraper = News_Scraper.NewsScraper("TSLA")
model = Model.Model()
newsScraper.retrieveNews()
newsHeadlines = newsScraper.returnNewsItems()
newsScraper.printNewsItems()
print("\n\n==================Predictions=======================")

predictions = model.predictHeadlines(newsHeadlines)
for prediction in predictions:
    print(prediction)