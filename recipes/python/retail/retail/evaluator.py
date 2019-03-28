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

class Evaluator(RegressionEvaluator):
    def __init__(self):
       print ("Initiate")

    def split(self, configProperties={}, dataframe=None):
        dataframe.date = pd.to_datetime(dataframe.date)
        dataframe['week'] = dataframe.date.dt.week
        dataframe['year'] = dataframe.date.dt.year

        df = pd.concat([dataframe, pd.get_dummies(dataframe['storeType'])], axis=1)
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
