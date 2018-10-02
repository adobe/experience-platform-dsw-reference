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

class Evaluator(AbstractEvaluator):
    def __init__(self):
       print ("initiate")

    def evaluate(self, data=[], config={}):
        print ("Evaluation evaluate triggered")
        y_pred = data['ml_score'].values
        y_actual = data['weeklySalesAhead'].values
        mape = np.mean(np.abs((y_actual - y_pred) / y_actual))

        metric = [{"name": "MAPE", "value": mape, "valueType": "double"}]

        return metric



    def split(self, config={}):
        print ("Split triggered")

        #########################################
        # Load Data
        #########################################
        prodreader = DataSetReader(client_id=configProperties['ML_FRAMEWORK_IMS_USER_CLIENT_ID'],
                                   user_token=configProperties['ML_FRAMEWORK_IMS_TOKEN'],
                                   service_token=configProperties['ML_FRAMEWORK_IMS_ML_TOKEN'])

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

        # Additional Split
        train_start = '2010-02-12'
        train_end = '2012-01-27'
        test_start = '2012-02-03'
        train = df[train_start:train_end]
        test = df[test_start:]

        print("Training Data Load Finish")

        return train, test


