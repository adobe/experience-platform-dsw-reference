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

from .helper import *
from sdk.data_loader import DataLoader
from pyspark.sql.functions import col


class TrainingDataLoader(DataLoader):
    logger = setupLogger(__name__)

    def load(self, config_properties, spark):
        if config_properties is None :
            raise ValueError("config_properties parameter is null")
        if spark is None:
            raise ValueError("spark parameter is null")

        tenant_id = str(config_properties.get("tenantId"))

        pd = load_dataset(config_properties, spark, tenant_id, "trainingDataSetId")
        self.logger.debug("Training data loader count is %s " % pd.count())

        return pd