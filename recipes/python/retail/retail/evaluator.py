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
import numpy as np
import pandas as pd

class Evaluator(AbstractEvaluator):
    def __init__(self):
       print ("Initiate")

    def split(self, configProperties={}, dataframe=None):

        train_start = '2010-02-12'
        train_end = '2012-01-27'
        val_start = '2012-02-03'
        train = dataframe[train_start:train_end]
        val = dataframe[val_start:]

        return train, val

    def evaluate(self, data=[], model={}, configProperties={}):
        print ("Evaluation evaluate triggered")
        val = data.drop('weeklySalesAhead', axis=1)
        y_pred = model.predict(val)
        y_actual = data['weeklySalesAhead'].values
        mape = np.mean(np.abs((y_actual - y_pred) / y_actual))
        mae = np.mean(np.abs(y_actual - y_pred))
        rmse = np.sqrt(np.mean((y_actual - y_pred) ** 2))

        metric = [{"name": "MAPE", "value": mape, "valueType": "double"},
                  {"name": "MAE", "value": mae, "valueType": "double"},
                  {"name": "RMSE", "value": rmse, "valueType": "double"}]

        return metric
