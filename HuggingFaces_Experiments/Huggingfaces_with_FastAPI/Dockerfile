# set base image
FROM python:3.8.10-slim

# author
author='Grigoriy Shmigol'

# metadata
LABEL version='1.0'
LABEL description="ML OPS 101"

WORKDIR ./HuggingFaces_Experiments/Huggingfaces_with_FastAPI/

COPY . /src

RUN pip install -r requirements.txt