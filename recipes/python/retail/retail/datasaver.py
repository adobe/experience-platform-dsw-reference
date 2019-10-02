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
from data_access_sdk_python.writer import DataSetWriter
import pandas as pd

def save(config_properties, prediction):
    print("Datasaver Start")
    print("Setting up Writer")

   
    writer = DataSetWriter(client_id=config_properties['ML_FRAMEWORK_IMS_USER_CLIENT_ID'],
                           user_token=config_properties['ML_FRAMEWORK_IMS_TOKEN'],
                           service_token=config_properties['ML_FRAMEWORK_IMS_ML_TOKEN'],
                           sandbox_id=configProperties['sandboxId'],
                           sandbox_name=configProperties['sandboxName'])

    print("Writer Configured")

    tenant_id = config_properties.get("tenantId")
    prediction = prediction.add_prefix(tenant_id+".")
    prediction = prediction.join(pd.DataFrame(
        {
            '_id': "",
            'timestamp': '2019-01-01T00:00:00',
            'eventType': ""
        }, index=prediction.index))

    writer.write(data_set_id=config_properties['scoringResultsDataSetId'],
                 dataframe=prediction,
                 ims_org=config_properties['ML_FRAMEWORK_IMS_TENANT_ID'],
                 file_format='json')

    print("Write Done")
    print("Datasaver Finish")
