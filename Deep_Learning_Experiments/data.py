# load dependacies
import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn.metrics import mean_squared_error
from matplotlib import pyplot


class DataLoader:
    """
    Arguments:
    - data_dir : Data directory which contains files mentioned above.
    - split_ratio : to decide length of training / test
    """
    ENTIRE_NUMBER = 69

    def __init__(self, data_dir, training_length, window_prev, mode):
        self.window_prev = window_prev
        self.data_dir = data_dir
        self.split_ratio = training_length
        self.mode = mode
        X_train, X_test, y_train, y_test = self.preproc_entire()
        self.X_train = X_train
        self.X_test = X_test
        self.y_train = y_train
        self.y_test = y_test

    def preproc_entire(self):
        dataset = self.preproc_csv()
        reframed = self.preproc_data_for_supervised(
            dataset,self.window_prev,
            1,
            dropnan=True,
            fillnan = False)

        values = reframed.values
        train_length = int(self.split_ratio * len(dataset))
        train = values[:train_length, :]
        if self.mode == 'predict':
            test = values[len(dataset)-self.window_prev-1, :]
        else:
            test = values[train_length:train_length + 1, :]

        # split into input and outputs
        n_obs =  self.window_prev * self.ENTIRE_NUMBER
        self.X_train, self.y_train = train[:, :n_obs], train[:, -self.ENTIRE_NUMBER:]
        self.X_test, self.y_test = test[:, :n_obs], test[:, -self.ENTIRE_NUMBER:]
        
        # reshape input to be 3D [samples, timesteps, features]
        train_X = self.X_train.reshape((train_X.shape[0], self.window_prev, self.ENTIRE_NUMBER ))
        test_X = self.X_test.reshape((test_X.shape[0], self.window_prev, self.ENTIRE_NUMBER))
        
        return train_X, test_X, train_y, test_y
        
        
    def preproc_csv(self):
        # read .csv raw file from datadirectory
        rawdata = pd.read_csv(self.data_dir)
        rawdata = rawdata.sort_values(by=['Unnamed: 0'], axis=0) # sort with ascending order
        raw_np = rawdata.to_numpy()
        raw_np_proc = raw_np[:,1:]

        # to construct one-hot encoded input dataset
        inputnp = np.zeros((len(raw_np), self.ENTIRE_NUMBER))
        i = 0
        for row in raw_np_proc:
            for elem in row:
                #assign one-hot values
                inputnp[i, elem-1] = 1
            i += 1
        return inputnp

    def preproc_data_for_supervised(self, data, n_in,
                                    n_out=1, dropnan = False,
                                    fillnan = True):
        ''' 
        Parameters
        ----------
        data : TYPE
            numpy array type time series data
        n_in : TYPE, optional
            DESCRIPTION. The default is 1.
        n_out : TYPE, optional
            DESCRIPTION. The default is 1.
        dropnan : TYPE, optional
            shifting values will generate nan value. handling the nan.

        '''
        n_in = self.window_prev

        n_vars = 1 if type(data) is list else data.shape[1]
        df = pd.DataFrame(data)
        cols, names = list(), list()

        # input sequence (t-n, ... t-1)
        for i in range(n_in, 0, -1):
            cols.append(df.shift(i))
            names += [('var%d(t-%d)' % (j+1, i)) for j in range(n_vars)]
        # forecast sequence (t, t+1, ... t+n)
        for i in range(0, n_out):
            cols.append(df.shift(-i))
            if i == 0:
                names += [('var%d(t)' % (j+1)) for j in range(n_vars)]
            else:
                names += [('var%d(t+%d)' % (j+1, i)) for j in range(n_vars)]

        # put it all together
        aggregated = pd.concat(cols, axis=1)
        aggregated.columns = names
        # drop rows with NaN values
        if dropnan:
            aggregated.dropna(inplace=True)
        if fillnan:
            aggregated.fillna(method = 'ffill')

        return aggregated
