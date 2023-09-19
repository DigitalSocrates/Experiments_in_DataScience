# imports
import pandas as pd
import numpy as np
import pmdarima as pm
from pmdarima import auto_arima
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
from utils import read_all_parquet_files
from model import Model
from trainer import Trainer


# dataset filename
DATASET_LOCAL_COPY = './../static/data/'
MODEL_LOCATION = './../static/model/'

# List of columns to forecast
COLUMNS_TO_FORECAST = ['Ball_Bonus'] #, 'Ball_1', 'Ball_2', 'Ball_3', 'Ball_4', 'Ball_5', 'Ball_Bonus'] #  

# read in lottery games data 
all_games = read_all_parquet_files(DATASET_LOCAL_COPY)

# need to convert data 
all_games['Ball_1'] = all_games['Ball_1'].astype('float64')
all_games['Ball_2'] = all_games['Ball_2'].astype('float64')
all_games['Ball_3'] = all_games['Ball_3'].astype('float64')
all_games['Ball_4'] = all_games['Ball_4'].astype('float64')
all_games['Ball_5'] = all_games['Ball_5'].astype('float64')
all_games['Ball_Bonus'] = all_games['Ball_Bonus'].astype('float64')

min_date = all_games['Date'].min()
max_date = all_games['Date'].max()

# sort by date
all_games.sort_values(by=['Date'], ascending=False, inplace=True)
# set index
all_games.set_index('Date', inplace=True)
# specify frequency IMPORTANT
all_games.index = pd.DatetimeIndex(all_games.index).to_period('3.5D')
all_games.sort_index(inplace=True)

# i do not htink that we care if the data is ordered
all_games = all_games.sample(frac=1).reset_index(drop=True)
"""from sklearn.utils import shuffle
df = shuffle(df)"""

# use first rows for training and use last row for out-of-sample testing
X_train_all_balls, X_test_all_balls = all_games.iloc[:, :6], all_games.iloc[[-1], :6]

# instantiate model trainer
trainer = Trainer()

models_for_each_ball = {}

# Perform a grid search to find the best ARIMA model
for column in COLUMNS_TO_FORECAST:
    ts_data = X_train_all_balls[column]

    try:
        # Use auto_arima to automatically select the best hyperparameters
        best_order, best_model = trainer.find_best_arima_model(ts_data=ts_data)

        # Fit the ARIMA model with the best hyperparameters
        arima_model, arima_model_fit = trainer.fit_arima_model(
            ts_data=ts_data,
            order=best_order
        )
        
        # Create an instance of the Model class
        my_model = Model(name=column,
                         model=arima_model,
                         model_fit=arima_model_fit,
                         order=best_order)
        
        arima_model_fit.save(f'{MODEL_LOCATION}{column}_model.pkl')
        with open(f'{MODEL_LOCATION}{column}_model_metadata.txt', 'w',encoding='UTF-8') as f:
            summary = arima_model_fit.summary().as_text()
            f.write(summary)

        models_for_each_ball[column] = my_model

    except Exception as e:
        print (f'Exception -> {e}')
        break
"""
print(models_for_each_ball)

# List of trained ARIMA models
arima_models = []

# Loop through each column and fit ARIMA models
for column in COLUMNS_TO_FORECAST:
    ts_data = all_games[column].astype(float)
    # get the best model from the previous step
    model = models_for_each_ball[column]
    arima_models.append(model)

    final_model = model.model
    final_model_fit = model.model_fit

    # Forecast the next data point
    #forecast = final_model_fit.predict(n_periods=len(ts_data),steps=1)
    # make one-day forecast
    forecast = final_model_fit.predict(n_periods=1, exog=None, return_conf_int=True)

    print(f"Forecast for ('{column}'): {forecast.iloc[0]:.2f}")

results = []
# Loop through each column and fit ARIMA models
for column in COLUMNS_TO_FORECAST:
    ts_data = all_games[column].astype(float)
    # Generate predictions from each ARIMA model
    result = 0
    for model in arima_models:
        final_model = model.model
        # model=final_model(ts_data, order=model.order)
        model_fit = model.model_fit

        # Forecast the next data point
        forecast = model_fit.predict(n_periods=1)
        #print(forecast[0])
        #print(forecast[-1])
        #forecast = final_model_fit.forecast()

        result += forecast[0]
    results.append(f'{column} -> {int(result/len(arima_models))}')

for x in results:
    print (x)
"""
"""
# load model
loaded = ARIMAResults.load('model.pkl')

"""
