""" FASTAPi app """
import os
import uvicorn
import transformers
import torch
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from transformers import AutoTokenizer

# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from settings import DATABASE_URL
from src.v1.utils.custom_logger import CustomLogger
from src.v1.text_generator import TextGenerator
from src.v1.utils.create_app import App
from src.v1.utils.error_handling import get_default_error_response
from src.v1.core.config \
    import API_PREFIX, APP_NAME, APP_VERSION, IS_DEBUG, DOCS_URL, DEFAULT_MODEL_PATH

# Create a custom logger
logger_initializer = CustomLogger(__name__)
logger = logger_initializer.get_logger()

# Set pytorch GPU memory limit
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "max_split_size_mb:4096"

class TextIn(BaseModel):
    text: str

# initialize App
App = App(DEFAULT_MODEL_PATH)

# initialize app
app = App.create_app(APP_NAME, APP_VERSION, IS_DEBUG, DOCS_URL)

# initialize sentiment and text generator pipelines
text_generator = TextGenerator()


# create request handler at the root endpoint
@app.get("/")
async def root():
    """default message to be displayed - could include version id, etc."""
    return JSONResponse(
        status_code=200,
        content={"status_code": 200, "message": "Sample ML OPs API is online"},
    )


@app.get("/text_generation/{text}", response_model=None)
async def generate_text(text: str) -> dict:
    """ takes user provided value and generates text
    this task will take a while (upward of a few minutes)
    """
    try:
        # generate prediction
        result = text_generator.generate_text(text)
        return JSONResponse(
            status_code=200,
            content={"status_code": 200, "message": f"{result}"},
        )
    except Exception as ex:
        logger.error("Exception occured %s", ex)
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
            generated_code = generated_code + f"Res: {seq['generated_text']}"
        result = {"response": f"{generated_code}", "code": 200}
        return result
    except Exception as ex:
        logger.error("Exception occured %s", ex)
        return get_default_error_response(status_code=500)


@app.post("/generate/{sample}")
async def generate(payload: TextIn):
    """test post"""
    result = f"{payload}"
    return {"result": result}


# run as a script
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
