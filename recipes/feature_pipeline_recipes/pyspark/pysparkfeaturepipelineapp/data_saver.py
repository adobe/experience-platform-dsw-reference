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

from sdk.data_saver import DataSaver
from pyspark.sql.types import StringType, TimestampType
from pyspark.sql.functions import col, lit, struct
from .helper import *


class MyDatasetSaver(DataSaver):

    def save(self, config_properties, prediction):
        spark_context = prediction._sc
        if config_properties is None:
            raise ValueError("config_properties parameter is null")
        if prediction is None:
            raise ValueError("prediction parameter is null")
        if spark_context is None:
            self.error = ValueError("spark_context parameter is null")
            raise self.error

        tenant_id = str(config_properties.get("tenantId"))

        scored_df = prediction.withColumn("date", col("date").cast(StringType()))
        scored_df.printSchema()
        scored_df = scored_df.withColumn(tenant_id, struct(col("date"), col("store"), col("prediction")))

        scored_df = scored_df.select(tenant_id)

        write_dataset(config_properties, spark_context, scored_df, "scoringResultsDataSetId")
