from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from starlette.requests import Request

from src.v1.core import security
from src.v1.models.payload import QAPredictionPayload
from src.v1.models.prediction import QAPredictionResult
from src.v1.utils.nlp import QAModel
from src.v1.utils.error_handling import get_default_error_response
from src.v1.sentiment_analysis import SentimentAnalysis
from src.v1.utils.custom_logger import CustomLogger
from src.v1.utils.check_gpu import get_gpu_info

# Create a custom logger
logger_initializer = CustomLogger(__name__)
logger = logger_initializer.get_logger()

router = APIRouter()

# initialize sentiment and text generator pipelines
sentiment_analysis = SentimentAnalysis()


@router.post("/question", response_model=QAPredictionResult, name="question")
def post_question(
    request: Request,
    # authenticated: bool = Depends(security.validate_request),
    block_data: QAPredictionPayload = None,
) -> QAPredictionResult:
    """ Retrieves an answer from context given a question """

    model: QAModel = request.app.state.model
    prediction: QAPredictionResult = model.predict(block_data)

    return prediction


@router.get("/sentiment/{sentiment}", response_model=None)
async def read_item(sentiment: str) -> dict:
    """ takes user provided value and determines sentiment """
    try:
        return JSONResponse(
            status_code=200,
            content={
                "status_code": 200,
                "msg": f"{sentiment_analysis.process_sentiment(sentiment)}",
            },
        )
    except Exception as ex:
        logger.error("Exception occured %s", ex)
        return get_default_error_response(status_code=500)


@router.get("/device_details")
async def sentiment_details():
    """ will return device information """

    try:
        return JSONResponse(
            status_code=200,
            content={
                "status_code": 200,
                "message": f"{get_gpu_info()}",
            },
        )
    except Exception as ex:
        logger.error("Exception occured %s", ex)
        return get_default_error_response()
