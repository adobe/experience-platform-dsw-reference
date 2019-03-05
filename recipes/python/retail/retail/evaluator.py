#####################################################################
# ADOBE CONFIDENTIAL
# ___________________
#
#  Copyright 2018 Adobe
#  All Rights Reserved.
#
# NOTICE:  All information contained herein is, and remains
# the property of Adobe and its suppliers, if any. The intellectual
# and technical concepts contained herein are proprietary to Adobe
# and its suppliers and are protected by all applicable intellectual
# property laws, including trade secret and copyright laws.
# Dissemination of this information or reproduction of this material
# is strictly forbidden unless prior written permission is obtained
# from Adobe.
#####################################################################
from ml.runtime.python.Interfaces.AbstractEvaluator import AbstractEvaluator
from data_access_sdk_python.reader import DataSetReader
from datetime import datetime, timedelta
import numpy as np
import pandas as pd

class Evaluator(AbstractEvaluator):
    def __init__(self):
       print ("Initiate")

    def evaluate(self, data=[], model={}, configProperties={}):
        print ("Evaluation evaluate triggered")
        test = data.drop('weeklySalesAhead', axis=1)
        y_pred = model.predict(test)
        y_actual = data['weeklySalesAhead'].values
        mape = np.mean(np.abs((y_actual - y_pred) / y_actual))
        mae = np.mean(np.abs(y_actual - y_pred))
        rmse = np.sqrt(np.mean((y_actual - y_pred) ** 2))

        metric = [{"name": "MAPE", "value": mape, "valueType": "double"},
                  {"name": "MAE", "value": mae, "valueType": "double"},
                  {"name": "RMSE", "value": rmse, "valueType": "double"}]

        return metric



    def split(self, configProperties={}):
        #########################################
        # Load Data
        #########################################
        prodreader = DataSetReader(client_id=configProperties['ML_FRAMEWORK_IMS_USER_CLIENT_ID'],
                                   user_token=configProperties['ML_FRAMEWORK_IMS_TOKEN'],
                                   service_token=configProperties['ML_FRAMEWORK_IMS_ML_TOKEN'])

        data_set_id = configProperties.get("dataSetId")
        timeframe = configProperties.get("timeframe")

        if (data_set_id is not None and timeframe is not None):
            date_before = datetime.utcnow().date()
            date_after = date_before - timedelta(minutes=int(timeframe))
            df = prodreader.load(data_set_id=data_set_id, ims_org=configProperties['ML_FRAMEWORK_IMS_TENANT_ID'],
                                 date_after=date_after, date_before=date_before)
        else:
            df = prodreader.load(data_set_id=configProperties['trainingDataSetId'],
                                 ims_org=configProperties['ML_FRAMEWORK_IMS_TENANT_ID'])

        #########################################
        # Data Preparation/Feature Engineering
        #########################################
        df.date = pd.to_datetime(df.date)
        df['week'] = df.date.dt.week
        df['year'] = df.date.dt.year

        df = pd.concat([df, pd.get_dummies(df['storeType'])], axis=1)
        df.drop('storeType', axis=1, inplace=True)
        df['isHoliday'] = df['isHoliday'].astype(int)

        df['weeklySalesAhead'] = df.shift(-45)['weeklySales']
        df['weeklySalesLag'] = df.shift(45)['weeklySales']
        df['weeklySalesDiff'] = (df['weeklySales'] - df['weeklySalesLag']) / df['weeklySalesLag']
        df.dropna(0, inplace=True)

        df = df.set_index(df.date)
        df.drop('date', axis=1, inplace=True)

        # Split
        train_start = '2010-02-12'
        train_end = '2012-01-27'
        test_start = '2012-02-03'
        train = df[train_start:train_end]
        test = df[test_start:]

        return train, test


