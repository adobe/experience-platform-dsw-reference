#####################################################################
# ADOBE CONFIDENTIAL
# ___________________
#
#  Copyright 2020 Adobe
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

from pyspark.sql.functions import unix_timestamp, from_unixtime, to_date, lit, col
from sdk.evaluation.regression import RegressionEvaluator
from .helper import setupLogger


class Evaluator(RegressionEvaluator):
    logger = setupLogger(__name__)

    def __init__(self):
        print("Initiate")

    def split(self, config_properties, dataframe):
        # Order by date and split the data
        train = dataframe.filter(dataframe["date"] <= lit('2012-01-27')).orderBy("date")
        test = dataframe.filter(dataframe["date"] > lit('2012-01-27')).orderBy("date")
        self.logger.debug("Training dataset count is %s " % train.count())
        self.logger.debug("Testing dataset count is %s " % test.count())
        return train, test

