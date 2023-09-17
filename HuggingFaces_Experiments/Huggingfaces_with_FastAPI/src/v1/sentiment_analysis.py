import src.v1.models.sentiment.sentiment_model as sm


class SentimentAnalysis:
    """ sentiment analysis using transformers pipeline """
    sentiment_model = None

    def __init__(self):
        self.sentiment_model = sm.SentimentModel.instance()

    def process_sentiment(self, statement: str):
        """ get sentiment from a user specified string """
        return self.sentiment_model.predict(statement)
