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

from pyspark.sql.types import StringType, TimestampType
from pyspark.sql.functions import col, lit, struct
import logging


def load_dataset(config_properties, spark, tenant_id, dataset_id):

    service_token = str(spark.sparkContext.getConf().get("ML_FRAMEWORK_IMS_ML_TOKEN"))
    user_token = str(spark.sparkContext.getConf().get("ML_FRAMEWORK_IMS_TOKEN"))
    org_id = str(spark.sparkContext.getConf().get("ML_FRAMEWORK_IMS_ORG_ID"))
    api_key = str(spark.sparkContext.getConf().get("ML_FRAMEWORK_IMS_CLIENT_ID"))

    dataset_id = str(config_properties.get(dataset_id))

    for arg in ['service_token', 'user_token', 'org_id', 'dataset_id', 'api_key']:
        if eval(arg) == 'None':
            raise ValueError("%s is empty" % arg)

    dataset_options = get_dataset_options(spark.sparkContext)

    pd = spark.read.format("com.adobe.platform.dataset") \
        .option(dataset_options.serviceToken(), service_token) \
        .option(dataset_options.userToken(), user_token) \
        .option(dataset_options.orgId(), org_id) \
        .option(dataset_options.serviceApiKey(), api_key) \
        .load(dataset_id)

    # Get the distinct values of the dataframe
    pd = pd.distinct()

    # Flatten the data
    if tenant_id in pd.columns:
        pd = pd.select(col(tenant_id + ".*"))

    return pd


def get_dataset_options(spark_context):
    dataset_options = spark_context._jvm.com.adobe.platform.dataset.DataSetOptions
    return dataset_options


def write_dataset(config_properties, sparkContext, dataframe, dataset_id):

    dataset_options = get_dataset_options(sparkContext)

    service_token = str(sparkContext.getConf().get("ML_FRAMEWORK_IMS_ML_TOKEN"))
    user_token = str(sparkContext.getConf().get("ML_FRAMEWORK_IMS_TOKEN"))
    org_id = str(sparkContext.getConf().get("ML_FRAMEWORK_IMS_ORG_ID"))
    api_key = str(sparkContext.getConf().get("ML_FRAMEWORK_IMS_CLIENT_ID"))

    output_dataset_id = str(config_properties.get(dataset_id))

    for arg in ['service_token', 'user_token', 'org_id', 'api_key', 'output_dataset_id']:
        if eval(arg) == 'None':
            raise ValueError("%s is empty" % arg)

    timestamp = "2019-01-01 00:00:00"
    dataframe = dataframe.withColumn("timestamp", lit(timestamp).cast(TimestampType()))
    dataframe = dataframe.withColumn("_id", lit("empty"))
    dataframe = dataframe.withColumn("eventType", lit("empty"))

    dataframe.write.format("com.adobe.platform.dataset") \
        .option(dataset_options.orgId(), org_id) \
        .option(dataset_options.serviceToken(), service_token) \
        .option(dataset_options.userToken(), user_token) \
        .option(dataset_options.serviceApiKey(), api_key) \
        .save(output_dataset_id)


def setupLogger(name):
    # create logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # create formatter
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s: %(message)s')

    # add formatter to ch
    ch.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(ch)

    return logger
