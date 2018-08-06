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


def load(configProperties):

    print("Training Data Load Start")

    #########################################
    # Extract fields from configProperties
    #########################################
    data = configProperties['data']
    train_start = configProperties['train_start']
    train_end = configProperties['train_end']


    #########################################
    # Load Data
    #########################################
    df = pd.read_csv(data)


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

    train = df[train_start:train_end]

    print("Training Data Load Finish")

    return train

