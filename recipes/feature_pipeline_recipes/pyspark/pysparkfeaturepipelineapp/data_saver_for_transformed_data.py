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
import pyspark.sql.functions as f


class DatasetSaverForTransformedData(DataSaver):
    logger = setupLogger(__name__)

    def nest_cols(self, rename_df, tenant_id):

        df_nested = rename_df.withColumn(tenant_id, f.struct(*([f.col(c).alias(c) for c in rename_df.columns])))\
                    .drop(*(c for c in rename_df.columns))
        return df_nested

    def save(self, config_properties, dataframe):

        spark_context = dataframe._sc

        if config_properties is None:
            raise ValueError("configProperties parameter is null")
        if dataframe is None:
            raise ValueError("prediction parameter is null")
        if spark_context is None:
            raise ValueError("spark_context parameter is null")

        tenant_id = str(config_properties.get("tenantId"))
        output_df = dataframe.withColumn("date", col("date").cast(StringType()))

        # Nest the columns within tenant id
        output_df = self.nest_cols(output_df, tenant_id)
        self.logger.debug("Transformed dataset count is %s " % output_df.count())

        write_dataset(config_properties, spark_context, output_df, "transformedDataSetId")



