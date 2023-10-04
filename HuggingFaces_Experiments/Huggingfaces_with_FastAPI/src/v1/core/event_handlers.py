from typing import Callable
from src.v1.utils.custom_logger import CustomLogger
from fastapi import FastAPI
from src.v1.utils.nlp import QAModel

# Set up custom logger
logger_initializer = CustomLogger(__name__)
logger = logger_initializer.get_logger()


def _startup_model(app: FastAPI, model_path: str) -> None:
    model_instance = QAModel(model_path)
    app.state.model = model_instance


def _shutdown_model(app: FastAPI) -> None:
    app.state.model = None


def start_app_handler(app: FastAPI, model_path: str) -> Callable:
    def startup() -> None:
        logger.info("Running app start handler.")
        _startup_model(app, model_path)

    return startup


def stop_app_handler(app: FastAPI) -> Callable:
    def shutdown() -> None:
        logger.info("Running app shutdown handler.")
        _shutdown_model(app)

    return shutdown
