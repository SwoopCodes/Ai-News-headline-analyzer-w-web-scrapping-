import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import datetime

class NewsScraper:

    def __init__(self, main_url):
        self.main_url = f"https://finance.yahoo.com/quote/{main_url}/news/"
        PATH = "./chromedriver.exe"
        service = Service(PATH)

        # Performance Options
        # By removing any of these:
        # you are significantly increasing the time of how long news items are retrieved
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--blink-settings=imagesEnabled=false")

        self.driver = webdriver.Chrome(service=service, options=options)
        self.newsItems = []

    def printNewsItems(self):
        if self.newsItems == []:
            print("No news items currently found... Try searching")
        else:
            for newsItem in self.newsItems:
                print(newsItem)

    def printPageTitle(self):
        self.driver.get(self.main_url)
        print(self.driver.title)
        self.driver.quit()

    def retrieveNews(self):
        self.driver.get(self.main_url)

        try:
            self.driver.find_element(By.CLASS_NAME, "accept-all").click()
        except:
            pass

        try:
            WebDriverWait(self.driver, 5).until(  # Increased to 10 seconds
                lambda d: d.find_elements(By.CSS_SELECTOR, "li.story-item h3.clamp")
            )
        except:
            pass

        pageTitle = self.driver.title
        if pageTitle == "Symbol Lookup from Yahoo Finance":
            self.driver.quit()
            return "Ticker not found"
        else:
            newsItems = self.driver.find_elements(By.CSS_SELECTOR, "li.story-item h3.clamp")
            newsItemsContainer = []

            for newsItem in newsItems:

                if newsItem.text != "":
                    newsItemsContainer.append(newsItem.text)

            self.newsItems = newsItemsContainer
            self.driver.quit()
            return "News headlines found and stored"



    def appendToNewsItemsLog(self):

        if self.newsItems != []:
            logLocation = "./logs/Collected_News_Items.txt"
            if os.path.exists(logLocation):
                file = open(logLocation, "a")
                file.write("==============================================================\n")
                file.write(f"Scrapped website: {self.main_url}\n")
                file.write(f"Date scrapped: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}\n")
                file.write("==============================================================\n\n")
                newsItems = self.newsItems

                for newsItem in newsItems:
                    file.write(newsItem + "\n")

                file.write("\n\n")
                file.close()
                print("News Items added to log file './logs/Collected_News_Items.txt'... ")
            else:
                file = open("./logs/Collected_News_Items.txt", "w")
                file.write("==============================================================\n")
                file.write(f"Scrapped website: {self.main_url}\n")
                file.write(f"Date scrapped: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}\n")
                file.write("==============================================================\n\n")
                newsItems = self.newsItems

                for newsItem in newsItems:
                    file.write(newsItem + "\n")

                file.write("\n")
                file.close()
                print("News Items added to log file './logs/Collected_News_Items.txt'... ")
        else:
            print("No news items found... Cannot store to logs")