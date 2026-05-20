import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

class Model:
    def __init__(self):
        self.training_data = pd.read_csv('./Training_Data/news_training_data.csv')

        model = Pipeline([
            ("tfidf", TfidfVectorizer()),
            ("clf", LogisticRegression()),
        ])
        self.model = model

    def predictHeadlines(self, newsHeadlines):

        if newsHeadlines == []:
            print("No headlines given...")
            return False


        X = self.training_data["headline"]
        Y = self.training_data["outcome"]

        self.model.fit(X, Y)
        predictions = self.model.predict(newsHeadlines)

        predictionsArray = []
        for headline, pred in zip(newsHeadlines, predictions):
            matchedHeadlinePrediction = (headline, pred.capitalize())
            predictionsArray.append(matchedHeadlinePrediction)

        return predictionsArray

    def calculateAccuracy(self):
        X = self.training_data["headline"]
        Y = self.training_data["outcome"]

        x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size = 0.3,)
        self.model.fit(x_train, y_train)
        predictions = self.model.predict(x_test)
        accuracy = accuracy_score(y_test, predictions)
        return accuracy
