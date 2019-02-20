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

from pyspark.ml import Pipeline
from pyspark.ml.regression import GBTRegressor
from pyspark.ml.feature import VectorAssembler

import numpy as np


def apply(configProperties):

    if(configProperties is None) :
        raise ValueError("configProperties parameter is null")

    input_features = str(configProperties.get("ACP_DSW_INPUT_FEATURES"))

    learning_rate = float(configProperties.get("learning_rate"))
    n_estimators = int(configProperties.get("n_estimators"))
    max_depth = int(configProperties.get("max_depth"))

    feature_list = list(input_features.split(","))
    feature_list.remove("date")
    feature_list.remove("storeType")

    cols = np.array(feature_list)

    # Gradient-boosted tree estimator
    gbt = GBTRegressor(featuresCol='features', labelCol='weeklySalesAhead', predictionCol='prediction',
                       maxDepth=max_depth, maxBins=n_estimators, stepSize=learning_rate)

    # Assemble the fields to a vector
    assembler = VectorAssembler(inputCols=cols, outputCol="features")

    # Construct the pipeline
    pipeline = Pipeline(stages=[assembler, gbt])

    return pipeline


def getParamMap(configProperties, sparkSession):
    return None