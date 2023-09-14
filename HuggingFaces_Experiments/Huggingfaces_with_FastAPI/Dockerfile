# set base image
FROM python:3.10.8-slim

# author
author='Grigoriy Shmigol'

# metadata
LABEL version='1.0'
LABEL description="Huggingfaces Experiments with FastAPI version 101"

# set working directory
WORKDIR ./HuggingFaces_Experiments/Huggingfaces_with_FastAPI/

# copy experiment files to the a destination folder
COPY . /src

# requirements installation
RUN pip install --upgrade pip & pip install -r requirements.txt

# download models (otherwise model(s) will be downloaded on the first use)
RUN python3 HuggingFaces_Experiments/Huggingfaces_with_FastAPI/src/v1/utils/download_model.py 124M
RUN python3 HuggingFaces_Experiments/Huggingfaces_with_FastAPI/src/v1/utils/download_model.py 355M
RUN python3 HuggingFaces_Experiments/Huggingfaces_with_FastAPI/src/v1/utils/download_model.py 774M
RUN python3 HuggingFaces_Experiments/Huggingfaces_with_FastAPI/src/v1/utils/download_model.py 1558M