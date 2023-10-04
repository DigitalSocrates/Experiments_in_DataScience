""" Config file """
APP_VERSION = '0.1.0'
APP_NAME = 'Sample ML OPs App'
API_PREFIX = '/api'
IS_DEBUG = True
DOCS_URL = '/docs'
DEFAULT_MODEL_PATH = 'src/static/models'

# config = Config(".env")
LOGGING_LEVEL = 'logging.DEBUG'

# API_KEY: Secret = config("API_KEY", cast=Secret)
# IS_DEBUG: bool = config("IS_DEBUG", cast=bool, default=False)

# DEFAULT_MODEL_PATH: str = config("DEFAULT_MODEL_PATH")
QUESTION_ANSWER_MODEL: str = 'deepset/roberta-base-squad2'
# config("QUESTION_ANSWER_MODEL")
