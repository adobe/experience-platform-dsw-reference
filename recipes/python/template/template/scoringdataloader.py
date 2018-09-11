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

def load(configProperties):
    # This variable will hold the part of the data on which we predict values
    test = None

    #########################################
    # Extract fields from configProperties
    #########################################
    # data = configProperties['data']
    # test_start = configProperties['test_start']

    print("Scoring Data Load Start")

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
    ### Then return the scoring data      ###
    # test = df[test_start:]

    print("Scoring Data Load Finish")

    return test
