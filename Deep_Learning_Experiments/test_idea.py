from keras.layers import Dense, Concatenate, LSTM, Input, Flatten
from keras.models import Model
from keras.utils import plot_model


look_back = 3200  # just for running the code I used this number

# Model architecture 

inputs = Input(shape=(1,look_back),name='Input_1')

lstm1 = LSTM(6, name='LSTM_1')(inputs)

lstm2 = LSTM(6, name='LSTM_2')(inputs)

concatenated = Concatenate( name='Concatenate_1')([lstm1,lstm2])

output1 = Dense(1, name='Dense_1')(concatenated)

model = Model(inputs=inputs, outputs=output1)

model.summary()

#plot_model(model)

from sklearn.datasets import make_blobs
train_x , train_y = make_blobs(n_samples=1000, centers=2, n_features=look_back,random_state=0)

train_x = train_x.reshape(train_x.shape[0], 1, train_x.shape[1])

model.compile(loss='mean_squared_error', optimizer='adam', metrics = ['mse'])
model.fit(train_x, train_y, epochs=5, batch_size=1, verbose=1)