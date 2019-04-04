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

    training_data_set_id = configProperties.get("trainingDataSetId")
    timeframe = configProperties.get("timeframe")

    if (timeframe is not None):
        date_before = datetime.utcnow().date()
        date_after = date_before - timedelta(minutes=int(timeframe))
        dataframe = prodreader.load(data_set_id=training_data_set_id, ims_org=configProperties['ML_FRAMEWORK_IMS_TENANT_ID'],
                             date_after=date_after, date_before=date_before)
    else:
        dataframe = prodreader.load(data_set_id=training_data_set_id,
                             ims_org=configProperties['ML_FRAMEWORK_IMS_TENANT_ID'])

    evaluator = Evaluator()
    (train_data, _) = evaluator.split(configProperties, dataframe)

    print("Training Data Load Finish")
    return train_data