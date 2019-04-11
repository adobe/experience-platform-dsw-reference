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
from ml.runtime.python.core.RegressionEvaluator import RegressionEvaluator
from data_access_sdk_python.reader import DataSetReader
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
from retail.utils import Utils

class Evaluator(RegressionEvaluator):
    def __init__(self):
       print ("Initiate")

    def split(self, configProperties={}, dataframe=None):

        if '_id' in dataframe.columns:
            #Rename columns to strip tenantId
            dataframe = dataframe.rename(columns = lambda x : str(x)[str(x).find('.')+1:])
            #Drop id, eventType and timestamp
            dataframe.drop(['_id', 'eventType', 'timestamp'], axis=1, inplace=True)


        dataframe.date = pd.to_datetime(dataframe.date)
        dataframe['week'] = dataframe.date.dt.week
        dataframe['year'] = dataframe.date.dt.year

        dataframe = pd.concat([dataframe, pd.get_dummies(dataframe['storeType'])], axis=1)
        dataframe.drop('storeType', axis=1, inplace=True)
        dataframe['isHoliday'] = dataframe['isHoliday'].astype(int)

        dataframe['weeklySalesAhead'] = dataframe.shift(-45)['weeklySales']
        dataframe['weeklySalesLag'] = dataframe.shift(45)['weeklySales']
        dataframe['weeklySalesDiff'] = (dataframe['weeklySales'] - dataframe['weeklySalesLag']) / dataframe['weeklySalesLag']
        dataframe.dropna(0, inplace=True)

        dataframe = dataframe.set_index(dataframe.date)
        dataframe.drop('date', axis=1, inplace=True)
        # Split
        train_start = '2010-02-12'
        train_end = '2012-01-27'
        test_start = '2012-02-03'
        train = dataframe[train_start:train_end]
        test = dataframe[test_start:]

        return train, test
