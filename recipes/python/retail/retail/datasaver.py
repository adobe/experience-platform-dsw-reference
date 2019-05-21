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

def save(configProperties, prediction):
    print("Datasaver Start")
    print("Setting up Writer")

    #catalog_url = "https://platform.adobe.io/data/foundation/catalog"
    #ingestion_url = "https://platform.adobe.io/data/foundation/import"

    # writer = DataSetWriter(catalog_url=catalog_url,
    #                       ingestion_url=ingestion_url,
    writer = DataSetWriter(client_id=configProperties['ML_FRAMEWORK_IMS_USER_CLIENT_ID'],
                           user_token=configProperties['ML_FRAMEWORK_IMS_TOKEN'],
                           service_token=configProperties['ML_FRAMEWORK_IMS_ML_TOKEN'])

    print("Writer Configured")

    tenantId = configProperties.get("tenantId")
    prediction = prediction.add_prefix(tenantId+".")
    prediction = prediction.join(pd.DataFrame(
        {
            '_id': "",
            'timestamp': '2019-01-01T00:00:00',
            'eventType': ""
        },  index=prediction.index))

    writer.write(data_set_id=configProperties['output_dataset_id'],
                 dataframe=prediction,
                 ims_org=configProperties['ML_FRAMEWORK_IMS_TENANT_ID'],
                 file_format='json')

    print("Write Done")
    print("Datasaver Finish")

