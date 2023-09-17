""" Text Generation Model """
import os
import logging
import torch
import mlflow
from transformers import pipeline
from transformers.generation import GenerationConfig
from transformers import GPTNeoForCausalLM, GPT2Tokenizer

# Create a custom logger
logger = logging.getLogger(__name__)


os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "max_split_size_mb:5012"


class TextGenerationModel(mlflow.pyfunc.PythonModel):
    """ text generation model using transformers pipeline  """
    text_generation_pipeline = None
    tokenizer = None
    model = None

    def __init__(self):
        raise RuntimeError('Call instance() instead')

    @classmethod
    def instance(cls, model_name: str = "EleutherAI/gpt-neo-2.7B",
                 max_length: int = 2096):
        """ initialize text generation pipeline """
        if cls.model is None:
            logger.info('Creating new instance')
            # set the device
            device = torch.device('cuda:0')
            # instantiate tokenizer
            cls.tokenizer = GPT2Tokenizer.from_pretrained(model_name)
            # instantiate model
            cls.model = GPTNeoForCausalLM.from_pretrained(model_name)
            cls.text_generation_pipeline = pipeline('text-generation',
                                                    model=cls.model,
                                                    tokenizer=cls.tokenizer,
                                                    device=device,
                                                    temperature=0.9,
                                                    do_sample=True,
                                                    max_length=max_length,
                                                    top_k = 50)
        return cls

    @classmethod
    def use_fillmask(cls):
        """ define fill mask - designed for text generation tasks """
        cls.fill_mask = pipeline(
            "fill-mask",
            model=cls.model,
            tokenizer=cls.tokenizer
        )

        print(cls.fill_mask(f"Hugging Face's DistilBert is a \
                            {cls.tokenizer.mask_token} model."))
        #return cls.fill_mask

    @classmethod
    def get_generation_config(cls) -> GenerationConfig:
        """ reveals the values that are different from the default """
        return cls.model.generation_config
