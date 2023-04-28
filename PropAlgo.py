import numpy as np
import pandas as pd
from prophet import Prophet
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

PASSWORD = os.getenv("PASSWORD")
USERNAME = os.getenv("USERNAME")

def return_pH_Data():

    cluster = MongoClient(
        f"mongodb+srv://{USERNAME}:" + PASSWORD + "@cluster0.afjudwt.mongodb.net/?retryWrites=true&w=majority")
    db = cluster["database"]
    collection = db["pH"]
    data = list(collection.find({}))
    data_pH = pd.DataFrame(data)
    print(data_pH.dtypes['time_stamp'])
    print(data_pH.head(10))
    data_pH['time_stamp'] = pd.to_datetime(data_pH['time_stamp'])
    data_pH = data_pH.drop(data_pH.columns[[0]], axis=1)
    return data_pH

def return_Ox_Data():

    cluster = MongoClient(
        f"mongodb+srv://{USERNAME}:" + PASSWORD + "@cluster0.afjudwt.mongodb.net/?retryWrites=true&w=majority")
    db = cluster["database"]
    collection = db["Ox"]
    data = list(collection.find({}))
    data_Ox = pd.DataFrame(data)
    data_Ox['time_stamp'] = pd.to_datetime(data_Ox['time_stamp'])
    data_Ox = data_Ox.drop(data_Ox.columns[[0]], axis=1)
    return data_Ox

def return_Cl_Data():

    cluster = MongoClient(
        f"mongodb+srv://{USERNAME}:" + PASSWORD + "@cluster0.afjudwt.mongodb.net/?retryWrites=true&w=majority")
    db = cluster["database"]
    collection = db["Cl"]
    data = list(collection.find({}))
    data_Cl = pd.DataFrame(data)
    data_Cl['time_stamp'] = pd.to_datetime(data_Cl['time_stamp'])
    data_Cl = data_Cl.drop(data_Cl.columns[[0]], axis=1)
    return data_Cl

def return_Turb_Data():

    cluster = MongoClient(
        f"mongodb+srv://{USERNAME}:" + PASSWORD + "@cluster0.afjudwt.mongodb.net/?retryWrites=true&w=majority")
    db = cluster["database"]
    collection = db["Turb"]
    data = list(collection.find({}))
    data_Turb = pd.DataFrame(data)
    data_Turb['time_stamp'] = pd.to_datetime(data_Turb['time_stamp'])
    data_Turb = data_Turb.drop(data_Turb.columns[[0]], axis=1)
    return data_Turb

def fit_predict_model(dataframe, interval_width=0.99, changepoint_range=0.8):
    m = Prophet(yearly_seasonality=False, weekly_seasonality=False,
                seasonality_mode='multiplicative',
                interval_width=interval_width,
                changepoint_range=changepoint_range)
    m = m.fit(dataframe)

    forecast = m.predict(dataframe)
    forecast['fact'] = dataframe['y'].reset_index(drop=True)
    print('Displaying Prophet plot')
    return forecast

def pred(index):
    if index == 0:
        data_pH = return_pH_Data()
        data_pH.columns = ['y', 'ds']
        return fit_predict_model(data_pH)
    elif index == 1:
        data_Ox = return_Ox_Data()
        data_Ox.columns = ['y', 'ds']
        return fit_predict_model(data_Ox)
    elif index == 2:
        data_Cl = return_Cl_Data()
        data_Cl.columns = ['y', 'ds']
        return fit_predict_model(data_Cl)
    elif index == 3:
        data_Trub = return_Turb_Data()
        data_Trub.columns = ['y', 'ds']
        return fit_predict_model(data_Trub)

def detect_anomalies_pH(forecast):
    forecasted = forecast[['ds', 'trend', 'yhat', 'yhat_lower', 'yhat_upper', 'fact']].copy()

    forecasted['anomaly'] = np.zeros(len(return_pH_Data()["pH"]))
    forecasted.loc[forecasted['fact'] > forecasted['yhat_upper'] - 1, 'anomaly'] = 1
    forecasted.loc[forecasted['fact'] < forecasted['yhat_lower'] + 1, 'anomaly'] = -1

    return forecasted.tail(15)

def detect_anomalies_Ox(forecast):
    forecasted = forecast[['ds', 'trend', 'yhat', 'yhat_lower', 'yhat_upper', 'fact']].copy()

    forecasted['anomaly'] = np.zeros(len(return_Ox_Data()["Dissolved Oxygen"]))
    forecasted.loc[forecasted['fact'] > forecasted['yhat_upper'] - 1, 'anomaly'] = 1
    forecasted.loc[forecasted['fact'] < forecasted['yhat_lower'] + 1, 'anomaly'] = -1

    return forecasted.tail(15)

def detect_anomalies_Cl(forecast):
    forecasted = forecast[['ds', 'trend', 'yhat', 'yhat_lower', 'yhat_upper', 'fact']].copy()

    forecasted['anomaly'] = np.zeros(len(return_Cl_Data()["Chlorine"]))
    forecasted.loc[forecasted['fact'] > forecasted['yhat_upper'] - 1, 'anomaly'] = 1
    forecasted.loc[forecasted['fact'] < forecasted['yhat_lower'] + 1, 'anomaly'] = -1

    return forecasted.tail(15)

def detect_anomalies_Turb(forecast):
    forecasted = forecast[['ds', 'trend', 'yhat', 'yhat_lower', 'yhat_upper', 'fact']].copy()

    forecasted['anomaly'] = np.zeros(len(return_Turb_Data()["Turbidity"]))
    forecasted.loc[forecasted['fact'] > forecasted['yhat_upper'] - 1, 'anomaly'] = 1
    forecasted.loc[forecasted['fact'] < forecasted['yhat_lower'] + 1, 'anomaly'] = -1

    return forecasted.tail(15)

def graph(index):
    if index == 0:
        return detect_anomalies_pH(pred(0))
    if index == 1:
        return detect_anomalies_Ox(pred(1))
    if index == 2:
        return detect_anomalies_Cl(pred(2))
    if index == 3:
        return detect_anomalies_Turb(pred(3))

