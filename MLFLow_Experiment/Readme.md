# To install MlFlow 
pip install mlflow

# To start MlFlow server
Run the following command
mlflow ui
or
mlflow server --default-artifact-root ./mlruns --host 127.0.0.0 --port 5000

go to http://127.0.0.1:5000
and verify that service is running

![Main Screen](static/MlFlow/MlFlow_Experiments.png)

# Experiments 

As i build models and train them, i started to use MlFlow to keep track of parameters, metrics and other useful information

Let us see what I mean
![Experiments Expanded](static/MlFlow/MlFlow_Experiments_Expanded.png)


## Datasets
![Experimen Datasets Expanded](static/MlFlow/MlFlow_Experiments_Expanded_Datasets.png)

## Parameters
![Experiment Parameters Expanded](static/MlFlow/MlFlow_Experiments_Expanded_Parameters.png)


## Metrics
![Experiment Metrics Expanded](static/MlFlow/MlFlow_Experiments_Expanded_Metrics.png)

## Tags
![Experiment Tags Expanded](static/MlFlow/MlFlow_Experiments_Expanded_Tags.png)

## Artifacts
![Experiment Artifacts Expanded](static/MlFlow/MlFlow_Experiments_Expanded_Artifacts.png)