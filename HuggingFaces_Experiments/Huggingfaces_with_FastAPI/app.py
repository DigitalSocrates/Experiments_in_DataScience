""" main application """
import logging
import uvicorn
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from transformers import AutoTokenizer
import transformers
import torch
#from sqlalchemy import create_engine
#from sqlalchemy.orm import sessionmaker
#from settings import DATABASE_URL

from src.v1.sentiment_analysis import SentimentAnalysis
from src.v1.text_generator import TextGenerator

#engine = create_engine(DATABASE_URL)
#Session = sessionmaker(bind=engine)


# initialize app
app = FastAPI(title="Sample ML OPs App", docs_url="/docs", version="0.0.1", debug=True)


# Create a custom logger
logger = logging.getLogger(__name__)


class TextIn(BaseModel):
    text: str


# initialize sentiment and text generator pipelines
sentiment_analysis = SentimentAnalysis()
text_generator = TextGenerator()


# create request handler at the root endpoint
@app.get("/")
async def root():
    """default message to be displayed - could include version id, etc."""
    return JSONResponse(
            status_code=200,
            content={"status_code": 200,
                     "message": "Sample ML OPs API is online"},
        )


@app.get("/sentiment_details")
async def sentiment_details():
    """will return some json for now"""

    try:
        return JSONResponse(
            status_code=200,
            content={"status_code": 200,
                     "message": f"{sentiment_analysis.sentiment_model.device}"},
        )
    except Exception as ex:
        logger.error('Exception occured %s', ex)
        return get_default_error_response()


@app.get("/sentiment/{sentiment}", response_model=None)
async def read_item(sentiment: str, q: str | None = None) -> dict:
    """takes user provided value and determines sentiment"""
    try:
        return JSONResponse(
            status_code=200,
            content={"status_code": 200,
                     "message": f"{sentiment_analysis.process_sentiment(sentiment)}"},
        )
    except Exception as ex:
        logger.error('Exception occured %s', ex)
        return get_default_error_response(status_code=500)


@app.get("/text_generation/{text}", response_model=None)
async def generate_text(text: str) -> dict:
    """ takes user provided value and generates text """
    try:
        # generate prediction
        result = text_generator.generate_text(text)
        return JSONResponse(
            status_code=200,
            content={"status_code": 200,
                    "message": f"{result}"},
        )
    except Exception as ex:
        logger.error('Exception occured %s', ex)
        return get_default_error_response(status_code=500)


@app.get("/code_generate/{function_body}")
async def generate_code(function_body: str):
    """takes users input and generates code"""

    tokenizer = AutoTokenizer.from_pretrained("codellama/CodeLlama-7b-hf")
    pipeline = transformers.pipeline(
        "text-generation",
        model="codellama/CodeLlama-7b-hf",
        torch_dtype=torch.float32,
        device_map="auto",
    )

    sequences = pipeline(
        function_body,
        do_sample=True,
        temperature=0.2,
        top_p=0.9,
        num_return_sequences=1,
        eos_token_id=tokenizer.eos_token_id,
        max_length=100,
    )

    try:
        generated_code = ""
        for seq in sequences:
            generated_code = generated_code + f"Result: {seq['generated_text']}"
        result = {"response": f"{generated_code}", "code": 200}
        return result
    except Exception as ex:
        logger.error('Exception occured %s', ex)
        return get_default_error_response(status_code=500)


@app.post("/generate/{sample}")
def generate(payload: TextIn):
    """test post"""
    result = f"{payload}"
    return {"result": result}


def get_default_error_response(status_code=500, message="Internal Server Error"):
    """ default error message template """
    return JSONResponse(
        status_code=status_code,
        content={"status_code": status_code, "message": message},
    )


# run as a script
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)