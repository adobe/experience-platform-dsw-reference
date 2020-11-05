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

from sdk.data_saver import DataSaver
from pyspark.sql.types import StringType, TimestampType
from pyspark.sql.functions import col, lit, struct
from .helper import *


class MyDatasetSaver(DataSaver):

    def save(self, config_properties, prediction):
        sparkContext = prediction._sc
        if config_properties is None:
            raise ValueError("configProperties parameter is null")
        if prediction is None:
            raise ValueError("prediction parameter is null")
        if sparkContext is None:
            raise ValueError("sparkContext parameter is null")

        PLATFORM_SDK_PQS_PACKAGE = "com.adobe.platform.query"

        service_token = str(sparkContext.getConf().get("ML_FRAMEWORK_IMS_ML_TOKEN"))
        user_token = str(sparkContext.getConf().get("ML_FRAMEWORK_IMS_TOKEN"))
        org_id = str(sparkContext.getConf().get("ML_FRAMEWORK_IMS_ORG_ID"))
        api_key = str(sparkContext.getConf().get("ML_FRAMEWORK_IMS_CLIENT_ID"))
        sandbox_name = str(sparkContext.getConf().get("sandboxName") or "")

        print("Sandbox name='{}'".format(sandbox_name))

        scored_dataset_id = str(config_properties.get("scoringResultsDataSetId"))
        tenant_id = str(config_properties.get("tenant_id"))
        timestamp = "2019-01-01 00:00:00"

        for arg in ['service_token', 'user_token', 'org_id', 'scored_dataset_id', 'api_key', 'tenant_id']:
            if eval(arg) == 'None':
                raise ValueError("%s is empty" % arg)

        scored_df = prediction.withColumn("date", col("date").cast(StringType()))
        scored_df = scored_df.withColumn(tenant_id, struct(col("date"), col("store"), col("prediction")))
        scored_df = scored_df.withColumn("timestamp", lit(timestamp).cast(TimestampType()))
        scored_df = scored_df.withColumn("_id", lit("empty"))
        scored_df = scored_df.withColumn("eventType", lit("empty"))

        query_options = get_query_options(sparkContext)

        if sandbox_name:
            scored_df.select(tenant_id, "_id", "eventType", "timestamp").write.format(PLATFORM_SDK_PQS_PACKAGE) \
                .option(query_options.userToken(), user_token) \
                .option(query_options.serviceToken(), service_token) \
                .option(query_options.imsOrg(), org_id) \
                .option(query_options.apiKey(), api_key) \
                .option(query_options.datasetId(), scored_dataset_id) \
                .option(query_options.sandboxName(), sandbox_name) \
                .save()
        else:
            scored_df.select(tenant_id, "_id", "eventType", "timestamp").write.format(PLATFORM_SDK_PQS_PACKAGE) \
                .option(query_options.userToken(), user_token) \
                .option(query_options.serviceToken(), service_token) \
                .option(query_options.imsOrg(), org_id) \
                .option(query_options.apiKey(), api_key) \
                .option(query_options.datasetId(), scored_dataset_id) \
                .save()
