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
import pandas as pd
from .utils import get_client_context
from datetime import datetime, timedelta
from platform_sdk.settings import QUERY_SERVICE_URL
from platform_sdk.dataset_reader import DatasetReader

def load(config_properties):
    print("Training Data Load Start")

    #########################################
    # Load Data
    #########################################
    print("QUERY_SERVICE_URL from platform sdk is ", QUERY_SERVICE_URL)
    client_context = get_client_context(config_properties)

    dataset_reader = DatasetReader(client_context, config_properties['trainingDataSetId'])

    timeframe = config_properties.get("timeframe")
    tenant_id = config_properties.get("tenant_id")

    if (timeframe is not None):
        date_before = datetime.utcnow().date()
        date_after = date_before - timedelta(minutes=int(timeframe))
        dataframe = dataset_reader.where(dataset_reader[tenant_id + '.date'].gt(str(date_after)).And(dataset_reader[tenant_id + '.date'].lt(str(date_before)))).read()
    else:
        dataframe = dataset_reader.read()

    #########################################
    # Data Preparation/Feature Engineering
    #########################################
    if '_id' in dataframe.columns:
        #Rename columns to strip tenantId
        dataframe = dataframe.rename(columns = lambda x : str(x)[str(x).find('.')+1:])
        #Drop id, eventType and timestamp
        dataframe.drop(['_id', 'eventType', 'timestamp'], axis=1, inplace=True)

    dataframe.head()
    print(dataframe)

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
