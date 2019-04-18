#####################################################################
# ADOBE CONFIDENTIAL
# ___________________
#
#  Copyright 2017 Adobe
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

import numpy as np
import pandas as pd
from data_access_sdk_python.reader import DataSetReader
from datetime import datetime, timedelta
from retail.evaluator import Evaluator


def load(configProperties):
    print("Training Data Load Start")

    #########################################
    # Load Data
    #########################################
    prodreader = DataSetReader(client_id=configProperties['ML_FRAMEWORK_IMS_USER_CLIENT_ID'],
                               user_token=configProperties['ML_FRAMEWORK_IMS_TOKEN'],
                               service_token=configProperties['ML_FRAMEWORK_IMS_ML_TOKEN'])

    timeframe = configProperties.get("timeframe")

    if (timeframe is not None):
        date_before = datetime.utcnow().date()
        date_after = date_before - timedelta(minutes=int(timeframe))
        dataframe = prodreader.load(data_set_id=configProperties['trainingDataSetId'], ims_org=configProperties['ML_FRAMEWORK_IMS_TENANT_ID'],
                             date_after=date_after, date_before=date_before)
    else:
        dataframe = prodreader.load(data_set_id=configProperties['trainingDataSetId'],
                             ims_org=configProperties['ML_FRAMEWORK_IMS_TENANT_ID'])

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

    print("Training Data Load Finish")
    return dataframe
