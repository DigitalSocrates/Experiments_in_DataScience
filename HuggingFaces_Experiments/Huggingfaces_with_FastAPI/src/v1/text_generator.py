""" text generation class using transformer pipelines """
import logging
import src.v1.models.text_generation.text_generation_model as tg


# Create a custom logger
logger = logging.getLogger(__name__)


class TextGenerator:
    """ text generation using transformers pipeline """
    text_generation_model = None

    def __init__(self, max_length:int=2096):
        # instantiate text generation model
        self.text_generation_model = tg.TextGenerationModel.instance(max_length=max_length)


    def generate_text(self, statement:str):
        """ get sentiment from a user specified string """
        # get output
        model_ouput = self.text_generation_model.text_generation_pipeline.predict(statement)
        return model_ouput
