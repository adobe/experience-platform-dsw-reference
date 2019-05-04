'''
 * ADOBE CONFIDENTIAL
 * ___________________
 *
 *  Copyright 2018 Adobe Systems Incorporated
 *  All Rights Reserved.
 *
 * NOTICE:  All information contained herein is, and remains
 * the property of Adobe Systems Incorporated and its suppliers,
 * if any.  The intellectual and technical concepts contained
 * herein are proprietary to Adobe Systems Incorporated and its
 * suppliers and are protected by all applicable intellectual property
 * laws, including trade secret and copyright laws.
 * Dissemination of this information or reproduction of this material
 * is strictly forbidden unless prior written permission is obtained
 * from Adobe Systems Incorporated.
'''

import json
from helper import setup_logger, http_request


LOGGER = setup_logger(__name__)
FILE_PATH = "../datasets/retail/XDM0.9.9.9/"
CONTENT_TYPE = "application/json"


def get_dataset_id(create_dataset_url, headers, dataset_title, schema_id):
    """
    Get the datasetId by making a POST Request to "/data/foundation/catalog/datasets?requestDataSource=true"
    :param create_dataset_url: url
    :param headers: headers
    :param dataset_title: dataset title
    :param schema_id: schema url
    :return: dataset id
    """
    data_for_create_dataset = {
        "schemaRef": {
            "id": schema_id,
            "contentType": "application/vnd.adobe.xed+json; version=1"
        },
        "name": dataset_title,
        "description": dataset_title,
        "fileDescription": {
            "persisted": True,
            "containerFormat": "parquet",
            "format": "json"
        },
        "aspect": "production"
    }
    headers["Accept"] = CONTENT_TYPE
    headers["Content-Type"] = CONTENT_TYPE
    res_text = http_request("post", create_dataset_url, headers, json.dumps(data_for_create_dataset))
    dataset_response = str(json.loads(res_text))
    LOGGER.debug("dataset_response is %s", dataset_response)
    dataset_id = dataset_response.split("@/dataSets/")[1].split("'")[0]
    LOGGER.debug("dataset_id = %s", dataset_id)
    return dataset_id


def get_batch_id(create_batch_url, headers, dataset_id):

    """
    Get the batchId by making a POST request to "/data/foundation/import/batches"
    :param create_batch_url:
    :param headers:
    :param dataset_id:
    :return: batch id
    """
    data_for_create_batch = {"datasetId": dataset_id}
    headers["Accept"] = CONTENT_TYPE
    headers["Content-Type"] = CONTENT_TYPE
    LOGGER.debug("Create batch url is %s", create_batch_url)
    res_text = http_request("post", create_batch_url, headers, json.dumps(data_for_create_batch))
    batch_id = json.loads(res_text)["id"]
    LOGGER.debug("batch_id = %s",  batch_id)
    return batch_id


def upload_file(create_batch_url, headers, file_with_tenant_id, dataset_id, batch_id):
    """
    Upload the data file to a batch of the dataset
    :param create_batch_url:
    :param headers:
    :param file_with_tenant_id:
    :param dataset_id:
    :param batch_id:
    """
    headers["Content-type"] = "application/octet-stream"
    headers["Connection"] = "keep-alive"
    contents = open(FILE_PATH + file_with_tenant_id, "r").read()
    upload_url = create_batch_url + "/" + batch_id + "/datasets/" + dataset_id + "/files/" + file_with_tenant_id
    LOGGER.debug("Upload url is %s", upload_url)
    http_request("put", upload_url, headers, contents)
    LOGGER.debug("Upload file success")


def upload_file_hardcoded(create_batch_url, headers, file_with_tenant_id, dataset_id, batch_id):
    """
    Upload the data file to a batch of the dataset
    :param create_batch_url:
    :param headers:
    :param file_with_tenant_id:
    :param dataset_id:
    :param batch_id:
    """
    headers["Content-type"] = "application/octet-stream"
    headers["Connection"] = "keep-alive"
    contents = open(FILE_PATH + file_with_tenant_id, "r").read()
    upload_url = create_batch_url + "/" + batch_id + "/datasets/" + dataset_id + "/files/" + file_with_tenant_id
    LOGGER.debug("Upload url is %s", upload_url)
    http_request("put", upload_url, headers, contents)
    LOGGER.debug("Upload file success")


def replace_tenant_id(file_with_tenant_id, tenant_id):
    """
    Util for a string replace of the tenantId
    :param file_with_tenant_id: Name of the json file with the tenant id
    :param tenant_id: tenant id to be replaced
    """

    original_file = open(FILE_PATH + "DSWRetailSalesForXDM0.9.9.9.json", 'r')
    new_file = open(FILE_PATH + file_with_tenant_id, 'w')
    for line in original_file:
        new_file.write(line.replace('_acpmlexploratoryexternal', tenant_id))
    original_file.close()
    new_file.close()


def close_batch(create_batch_url, headers, batch_id):
    """
    Close the batch by making a POST request to "/data/foundation/import/batches"
    :param create_batch_url:
    :param headers:
    :param batch_id:
    """
    close_batch__url = create_batch_url + "/" + batch_id + "?action=COMPLETE"
    http_request("post", close_batch__url, headers)
