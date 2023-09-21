""" Sentiment Model """
import logging
import torch
from transformers import pipeline

# Create a custom logger
logger = logging.getLogger(__name__)


class SentimentModel:
    """ sentiment model using transformers pipeline  """
    sentiment_pipeline = None
    device = torch.device('cuda:0')

    def __init__(self):
        raise RuntimeError('Call instance() instead')

    @classmethod
    def instance(cls,
                 model: str =
                 "distilbert-base-uncased-finetuned-sst-2-english"):
        """ initialize sentiment model """
        if cls.sentiment_pipeline is None:
            logger.info('Creating new instance')
            # cls.sentiment_pipeline = cls.__new__(cls)
            cls.sentiment_pipeline = pipeline("sentiment-analysis",
                                              model=model,
                                              device=cls.device)
        # oracle = pipeline("question-answering",
        # model="distilbert-base-cased-distilled-squad",
        # tokenizer="bert-base-cased")
        return cls.sentiment_pipeline
