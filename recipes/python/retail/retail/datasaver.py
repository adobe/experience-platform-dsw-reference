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

import pandas as pd
from .utils import get_client_context
from platform_sdk.models import Dataset
from platform_sdk.dataset_writer import DatasetWriter

def save(config_properties, prediction):
    print("Datasaver Start")
    print("Setting up Writer")

    client_context = get_client_context(config_properties)

    tenant_id = config_properties.get("tenantId")
    prediction = prediction.add_prefix(tenant_id+".")

    prediction = prediction.join(pd.DataFrame(
        {
            '_id': "",
            'timestamp': '2019-01-01T00:00:00',
            'eventType': ""
        }, index=prediction.index))


    dataset = Dataset(client_context).get_by_id(config_properties['scoringResultsDataSetId'])
    dataset_writer = DatasetWriter(client_context, dataset)
    dataset_writer.write(prediction, file_format='json')
    print("Writer Configured")
    print("Write Done")
    print("Datasaver Finish")
