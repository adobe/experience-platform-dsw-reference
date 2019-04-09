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

from pyspark.sql.functions import lit
from .helper import *
import datetime


def load(configProperties, spark):

    if configProperties is None :
        raise ValueError("configProperties parameter is null")
    if spark is None:
        raise ValueError("spark parameter is null")

    pd = load_dataset(configProperties, spark, "trainingDataSetId")
    pd = prepare_dataset(pd)

    # Split the data
    timeframe = str(configProperties.get("timeframe"))
    if timeframe != 'None' :
      filterByTime = str(datetime.datetime.now() - datetime.timedelta(minutes = int(timeframe)))
      train = pd.filter(pd["tx_date"] >= lit(str(filterByTime)))
      print("Number of rows after filtering : " + str(train.count()))
    else :
      train = pd.filter(pd["tx_date"] <= lit('2012-01-27'))

    return train