'''
 * ADOBE CONFIDENTIAL
 * ___________________
 *
 *  Copyright 2019 Adobe Systems Incorporated
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
from utils import setup_logger, http_request


LOGGER = setup_logger(__name__)
FILE_PATH = "../datasets/retail/XDM0.9.9.9/"
CONTENT_TYPE = "application/json"


def get_dataset_id(create_dataset_url, headers, dataset_title, schema_id, data):
    """
    Get the datasetId by making a POST Request to "/data/foundation/catalog/datasets?requestDataSource=true"
    :param create_dataset_url: url
    :param headers: headers
    :param dataset_title: dataset title
    :param schema_id: schema url
    :param data: post request data
    :return: dataset id
    """

    # Set the title and description
    data['name'] = dataset_title
    data['description'] = dataset_title

    # Set the schema id
    data["schemaRef"]["id"] = schema_id

    headers["Accept"] = CONTENT_TYPE
    headers["Content-Type"] = CONTENT_TYPE
    res_text = http_request("post", create_dataset_url, headers, json.dumps(data))
    dataset_response = str(json.loads(res_text))
    LOGGER.debug("dataset_response is %s", dataset_response)
    dataset_id = dataset_response.split("@/dataSets/")[1].split("'")[0]
    LOGGER.debug("dataset_id = %s", dataset_id)
    return dataset_id


def get_batch_id(create_batch_url, headers, dataset_id, data):

    """
    Get the batchId by making a POST request to "/data/foundation/import/batches"
    :param create_batch_url: url
    :param headers: headers
    :param dataset_id: dataset id
    :param data: post request data
    :return: batch id
    """
    data["datasetId"] = dataset_id
    headers["Accept"] = CONTENT_TYPE
    headers["Content-Type"] = CONTENT_TYPE
    LOGGER.debug("Create batch url is %s", create_batch_url)
    res_text = http_request("post", create_batch_url, headers, json.dumps(data))
    batch_id = json.loads(res_text)["id"]
    LOGGER.debug("batch_id = %s",  batch_id)
    return batch_id


def upload_file(create_batch_url, headers, file_with_tenant_id, dataset_id, batch_id):
    """
    Upload the data file to a batch of the dataset
    :param create_batch_url: url
    :param headers: headers
    :param file_with_tenant_id: file name
    :param dataset_id: dataset id
    :param batch_id: batch id
    """
    headers["Content-type"] = "application/octet-stream"
    headers["Connection"] = "keep-alive"
    contents = open(FILE_PATH + file_with_tenant_id, "r").read()
    upload_url = create_batch_url + "/" + batch_id + "/datasets/" + dataset_id + "/files/" + file_with_tenant_id
    LOGGER.debug("Upload url is %s", upload_url)
    http_request("put", upload_url, headers, contents)
    LOGGER.debug("Upload file success")


def replace_tenant_id(original_file, file_with_tenant_id, tenant_id):
    """
    Util for a string replace of the tenantId
    :param original_file: Name of the original file whose tenant id needs to be replaced
    :param file_with_tenant_id: Name of the json file with the tenant id
    :param tenant_id: tenant id to be replaced
    """

    original_file = open(FILE_PATH + original_file, 'r')
    new_file = open(FILE_PATH + file_with_tenant_id, 'w')
    for line in original_file:
        new_file.write(line.replace('_acpmlexploratoryexternal', tenant_id))
    original_file.close()
    new_file.close()


def close_batch(create_batch_url, headers, batch_id):
    """
    Close the batch by making a POST request to "/data/foundation/import/batches"
    :param create_batch_url: url
    :param headers: headers
    :param batch_id: batch id
    """
    close_batch__url = create_batch_url + "/" + batch_id + "?action=COMPLETE"
    http_request("post", close_batch__url, headers)
