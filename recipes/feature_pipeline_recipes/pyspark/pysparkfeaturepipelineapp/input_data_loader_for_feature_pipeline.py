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

from .helper import setupLogger, load_dataset
from sdk.data_loader import DataLoader


class InputDataLoaderForFeaturePipeline(DataLoader):

    logger = setupLogger(__name__)

    def load(self, config_properties, spark):
        if config_properties is None:
            raise ValueError("configProperties parameter is null")
        if spark is None:
            raise ValueError("spark parameter is null")

        tenant_id = str(config_properties.get("tenantId"))
        pd = load_dataset(config_properties, spark, tenant_id, "inputDataSetId")
        self.logger.debug("Input dataset count is %s " % pd.count())
        return pd