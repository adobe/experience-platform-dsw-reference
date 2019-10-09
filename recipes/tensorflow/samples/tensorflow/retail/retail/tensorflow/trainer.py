#####################################################################
# ADOBE CONFIDENTIAL
# ___________________
#
#  Copyright 2019 Adobe
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

from ml.runtime.python.Interfaces.AbstractTrainer import AbstractTrainer
from platform_sdk.dataset_reader import DatasetReader
from platform_sdk.settings import QUERY_SERVICE_URL
from .utils import get_client_context

import numpy as np
import pandas as pd

import tensorflow as tf
fc = tf.feature_column
tf.set_random_seed(123)

import os
import json
import pickle

class Trainer(AbstractTrainer):
    def train(self, config={}):
        #########################################
        # Set Up
        #########################################
        tf.logging.set_verbosity(tf.logging.ERROR)
        tf_config = json.loads(os.environ['TF_CONFIG'])
        tf_config = json.loads('{}')
        os.environ['TF_CONFIG'] = json.dumps(tf_config)



        #########################################
        # Load Data
        #########################################

        client_context = get_client_context(config)

        dataset_reader = DatasetReader(client_context, config['trainingDataSetId'])
        dataframe = dataset_reader.read()

        #########################################
        # Data Preparation/Feature Engineering
        #########################################
        if '_id' in dataframe.columns:
            # Rename columns to strip tenantId
            dataframe = dataframe.rename(columns=lambda x: str(x)[str(x).find('.') + 1:])
            # Drop id, eventType and timestamp
            dataframe.drop(['_id', 'eventType', 'timestamp'], axis=1, inplace=True)

        dataframe.date = pd.to_datetime(dataframe.date)
        dataframe['week'] = dataframe.date.dt.week
        dataframe['year'] = dataframe.date.dt.year

        dataframe = dataframe.sort_values(by=['date', 'store'])

        dataframe = pd.concat([dataframe, pd.get_dummies(dataframe['storeType'])], axis=1)
        dataframe.drop('storeType', axis=1, inplace=True)
        dataframe['isHoliday'] = dataframe['isHoliday'].astype(int)

        dataframe['weeklySalesAhead'] = dataframe.shift(-45)['weeklySales']
        dataframe['weeklySalesLag'] = dataframe.shift(45)['weeklySales']
        dataframe['weeklySalesDiff'] = (dataframe['weeklySales'] - dataframe['weeklySalesLag']) / dataframe[
            'weeklySalesLag']
        dataframe.dropna(0, inplace=True)

        dataframe = dataframe.set_index(dataframe.date)
        dataframe.drop('date', axis=1, inplace=True)




        #########################################
        # Train / Validation Split
        #########################################
        train_start = '2010-02-12'
        train_end = '2012-01-27'
        val_start = '2012-02-03'
        train = dataframe[train_start:train_end]
        val = dataframe[val_start:]

        X_train = train.drop('weeklySalesAhead', axis=1)
        y_train = train['weeklySalesAhead'].values

        X_val = val.drop('weeklySalesAhead', axis=1)
        y_val = val['weeklySalesAhead'].values

        features = []
        for feature in X_train.columns:
            features.append(fc.numeric_column(feature, dtype=tf.float32))

        def gen_input_fn(features, labels, epochs=10, shuffle=True, batch_size=32):
            def input_function():
                dataset = tf.data.Dataset.from_tensor_slices((dict(features), labels))
                if shuffle:
                    dataset = dataset.shuffle(1000)
                dataset = dataset.batch(batch_size).repeat(epochs)
                return dataset
            return input_function

        train_input_fn = gen_input_fn(X_train, y_train)
        eval_input_fn = gen_input_fn(X_val, y_val, shuffle=False, epochs=1)



        #########################################
        # BoostedTreesRegressor Model
        #########################################
        learning_rate = float(config['learning_rate'])
        n_estimators = int(config['n_estimators'])
        max_depth = int(config['max_depth'])

        filename = config['modelPATH'] + '/my_model'
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        model = tf.estimator.BoostedTreesRegressor(features,
                                                   model_dir=filename,
                                                   n_batches_per_layer=5,
                                                   n_trees=n_estimators,
                                                   max_depth=max_depth,
                                                   learning_rate=learning_rate)

        model.train(train_input_fn, max_steps=n_estimators)



        #########################################
        # Process Metrics
        #########################################
        pred_dict = list(model.predict(eval_input_fn))
        y_pred = pd.Series([pred['predictions'][0] for pred in pred_dict])

        mape = np.mean(np.abs((y_val - y_pred) / y_val))
        mae = np.mean(np.abs(y_val - y_pred))
        rmse = np.sqrt(np.mean((y_val - y_pred) ** 2))

        metrics_dict = {}
        metrics_dict['MAPE'] = round(mape, 3)
        metrics_dict['MAE'] = round(mae, 3)
        metrics_dict['RMSE'] = round(rmse, 3)

        pickle.dump(metrics_dict, open(os.path.join(config['modelPATH'], 'metrics_dict.pkl'), 'wb'))