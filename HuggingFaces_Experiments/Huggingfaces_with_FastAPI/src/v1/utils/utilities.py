import os
import typing as t
from src.v1.utils.custom_logger import CustomLogger
from pathlib import Path
import torch
from transformers import AutoModelForQuestionAnswering, AutoTokenizer

# Set up custom logger
logger_initializer = CustomLogger(__name__)
logger = logger_initializer.get_logger()

class ModelLoader:
    """ModelLoader
    Downloading and Loading Hugging FaceModels
       Download occurs only when model is not located in the local model directory
       If model exists in local directory, load.
    """
    def __init__(
        self,
        model_name: str,
        model_directory: str,
        tokenizer_loader: AutoTokenizer,
        model_loader: AutoModelForQuestionAnswering,
    ):
        self.model_name = Path(model_name)
        self.model_directory = Path(model_directory)
        self.model_loader = model_loader
        self.tokenizer_loader = tokenizer_loader

        self.save_path = os.path.join(self.model_directory,self.model_name)
        logger.info("[+] Path %s", self.save_path)

        if not os.path.isdir(self.save_path):
            # we running for the first time so need to download the model
            logger.info("[+] %s does not exit!", self.save_path)
            os.makedirs(self.save_path, exist_ok=True)
            self.__download_model()

        self.tokenizer, self.model = self.__load_model()

    def __repr__(self):
        return f"{self.__class__.__name__}(model={self.save_path})"

    def __download_model(self) -> None:
        ''' Download model from HuggingFace
        '''
        logger.info("[+] Downloading %s", self.model_name)
        tokenizer = self.tokenizer_loader.from_pretrained(self.model_name)
        model = self.model_loader.from_pretrained(self.model_name)

        logger.info("[+] Saving %s to %s", self.model_name, self.save_path)
        tokenizer.save_pretrained(self.save_path)
        model.save_pretrained(self.save_path)

        logger.info("[+] Process completed")

    # Load model
    def __load_model(self) -> t.Tuple:

        logger.info("[+] Loading model from %s", self.save_path)
        tokenizer = self.tokenizer_loader.from_pretrained(self.save_path)
        # Check if GPU is available
        device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info("[+] Model loaded in %s complete", device)
        model = self.model_loader.from_pretrained(self.save_path).to(device)

        logger.debug("[+] Loading completed")
        return tokenizer, model

    def retrieve(self) -> t.Tuple:
        """Retriver

        Returns:
            Tuple: tokenizer, model
        """
        return self.tokenizer, self.model
