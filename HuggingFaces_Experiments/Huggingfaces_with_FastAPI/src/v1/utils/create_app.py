from fastapi import FastAPI
from src.v1.routes.router import api_router  # Import your API router
from src.v1.core.event_handlers import start_app_handler, stop_app_handler
from src.v1.utils.custom_logger import CustomLogger

# Set up custom logger
logger_initializer = CustomLogger(__name__)
logger = logger_initializer.get_logger()

class App:
    def __init__(self, default_model_path : str):
        self.model_path = default_model_path

    def create_app(self, name : str, version : str, is_debug : bool, docs_url : str) -> FastAPI:
        """
        Create a FastAPI application instance with configured settings.
        """
        self.app = FastAPI(
            title=name,
            version=version,
            debug=is_debug,
            docs_url=docs_url,
        )

        self.configure_app()  # Configure application settings
        self.configure_event_handlers()  # Configure event handlers

        return self.app

    def configure_app(self) -> None:
        """
        Configure the FastAPI application by including routers and other settings.
        """
        self.app.include_router(api_router, prefix="/api")

    def configure_event_handlers(self) -> None:
        """
        Configure startup and shutdown event handlers for the FastAPI application.
        """
        self.app.add_event_handler("startup", start_app_handler(self.app, self.model_path))
        self.app.add_event_handler("shutdown", stop_app_handler(self.app))

    def start_app(self) -> None:
        """
        Startup event handler for the FastAPI application.
        """
        # Your startup logic here

    def stop_app(self) -> None:
        """
        Shutdown event handler for the FastAPI application.
        """
        # Your shutdown logic here
