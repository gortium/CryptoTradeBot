from keras.models import Sequential
from keras.layers import LSTM, Dense
from DataManager import DataManager
import keras
import tensorflow as tf
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import time

path = "models/"
number = 1
model_name = "LSTM" + str(number)
fullpath = path + model_name 
load_model = True
n = 3   # timestep before
m = 1   # timestep to predict
period = 5
batch_size = 256
epoch = 100

# Data generation 
data_manager = DataManager()
df = data_manager.update_raw_data("coinfield", "btccad", period)
df = data_manager.add_feature_return(df)
df = data_manager.add_feature_log_return(df)
df.dropna(inplace=True)
x = np.array(df[["Close", "log_return"]].values)
scaler = MinMaxScaler(feature_range=(0, 1), copy=False).fit(x)
scaler.transform(x)
x_train, y_train, x_test, y_test = data_manager.get_training_and_testing_data(n, m, x)

# Model generation
if load_model:
    model = keras.models.load_model(fullpath)
else:
    model = Sequential()
    model.add(LSTM(4, input_shape=(x_train.shape[1], x_train.shape[2])))
    model.add(Dense(1))
    model.compile(loss="mean_squared_error", optimizer="adam")
    model.fit(x_train, y_train, epochs=epoch, validation_data=(x_test, y_test), batch_size=batch_size, verbose=1) 
    if not os.path.exists(path):
        os.makedirs(path)
    model.save(fullpath)

model.summary()

# Predict
train_predict = model.predict(x_train)
test_predict = model.predict(x_test)

# Zero pading
train_predict = np.c_[train_predict, np.zeros(train_predict.shape)]
test_predict = np.c_[test_predict, np.zeros(test_predict.shape)]

# Invert scaling
scaler.inverse_transform(train_predict)
train_predict = [x[0] for x in train_predict]

scaler.inverse_transform([x[0] for x in x_train])
x_train = [x[0][0] for x in x_train]

scaler.inverse_transform(test_predict)
test_predict = [x[0] for x in test_predict]

scaler.inverse_transform([x[0] for x in x_test])
x_test = [x[0][0] for x in x_test]

# Mean square error score
train_score = mean_squared_error(x_train, train_predict, squared=False)
test_score = mean_squared_error(x_test, test_predict, squared=False)

# Live validation
while(1):
    # Latest prices
    df = data_manager.update_raw_data("coinfield", "btccad", period).tail(n+1)
    latest_price = df["Close"].tail(1).values[0]
    latest_prices_plot.append(latest_price)
    latest_timestep = int((df.tail(1).index.astype(np.int64)/10**9)[0])
    latest_timestamps_plot.append(latest_timestep)
    df = data_manager.add_feature_return(df)
    df = data_manager.add_feature_log_return(df)
    df.dropna(inplace=True)
    x_live = np.array(df[["Close", "log_return"]].values)
    
    # Make new prediction
    scaler.transform(x_live)
    latest_predict = model.predict(np.array([x_live]))
    latest_predict = np.c_[latest_predict, np.zeros(latest_predict.shape)]
    scaler.inverse_transform(latest_predict)
    latest_predictons_plot.append(latest_predict[0][0])
    
    # Plot
    plt.plot(latest_timestamps_plot, latest_prices_plot, "ro", latest_timestamps_plot, latest_predictons_plot, "bo")
    plt.ioff()
    plt.show(block=False)
    
    # Wait period
    time.sleep(60*5.1*m)


