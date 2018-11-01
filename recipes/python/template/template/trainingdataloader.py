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

from template.evaluator import Evaluator

def load(configProperties):
    print("Training Data Load Start")
    evaluator = Evaluator()
    (train, _) = evaluator.split(configProperties)

    #########################################
    # Extract fields from configProperties
    #########################################
    # data = configProperties['data']
    # train_start = configProperties['train_start']
    # train_end = configProperties['train_end']


    #########################################
    # Load Data
    #########################################

    ### From CSV ###
    # df = pd.read_csv(data)

    ### - OR - From Data Access SDK ###
    # prodreader = DataSetReader(ims_url=configProperties['ims_url'],
    #                            catalog_url=configProperties['catalog_url'],
    #                            client_id=configProperties['client_id'],
    #                            client_secret=configProperties['client_secret'],
    #                            code=configProperties['code'])

    # df = prodreader.load(configProperties['data_set_id'], configProperties['ims_org'])

    #########################################
    # Data Preparation/Feature Engineering
    #########################################

    ### Add/Remove/Modify DataFrame below ###
    ### Then return the training data     ###
    # test = df[train_start:train_end]

    print("Training Data Load Finish")

    return train
