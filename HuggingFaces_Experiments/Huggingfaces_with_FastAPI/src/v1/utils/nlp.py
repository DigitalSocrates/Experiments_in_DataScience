import os
import torch
from typing import Dict, List

from transformers import AutoTokenizer
from transformers import AutoModelForQuestionAnswering
from transformers import pipeline

from src.v1.utils.custom_logger import CustomLogger
from src.v1.models.payload import QAPredictionPayload
from src.v1.models.prediction import QAPredictionResult
from src.v1.utils.utilities import ModelLoader
from src.v1.core.messages import NO_VALID_PAYLOAD
from src.v1.core.config import (
    DEFAULT_MODEL_PATH,
    QUESTION_ANSWER_MODEL,
)

# Create a custom logger
logger_initializer = CustomLogger(__name__)
logger = logger_initializer.get_logger()

# Set pytorch GPU memory limit
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "max_split_size_mb:4096"


class QAModel(object):
    device = torch.device('cuda:0')
    
    def __init__(self, path=DEFAULT_MODEL_PATH):
        self.path = path
        self._load_local_model()

    def _load_local_model(self):
        logger.info("[+] loading local model %s %s to path %s",
                    QUESTION_ANSWER_MODEL, DEFAULT_MODEL_PATH, self.path)
        tokenizer, model = ModelLoader(
            model_name=QUESTION_ANSWER_MODEL,
            model_directory=DEFAULT_MODEL_PATH,
            tokenizer_loader=AutoTokenizer,
            model_loader=AutoModelForQuestionAnswering,
        ).retrieve()

        self.nlp = pipeline("question-answering",
                            model=model,
                            tokenizer=tokenizer,
                            device=self.device)

    def _pre_process(self, payload: QAPredictionPayload) -> List:
        logger.info("Pre-processing payload.")
        result = [payload.context, payload.question]
        return result

    def _post_process(self, prediction: Dict) -> QAPredictionResult:
        logger.info("Post-processing prediction.")

        qa = QAPredictionResult(**prediction)

        return qa

    def _predict(self, features: List) -> tuple:
        logger.info("Predicting.")

        context, question = features

        QA_input = {
            "question": question,
            "context": context,
        }

        prediction_result = self.nlp(QA_input)

        return prediction_result

    def predict(self, payload: QAPredictionPayload):
        if payload is None:
            raise ValueError(NO_VALID_PAYLOAD.format(payload))

        pre_processed_payload = self._pre_process(payload)
        prediction = self._predict(pre_processed_payload)
        logger.info(prediction)
        post_processed_result = self._post_process(prediction)

        return post_processed_result
