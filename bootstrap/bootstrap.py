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


import requests
import yaml
from utils import setup_logger

from data_ingester import get_dataset_id, get_batch_id, upload_file, replace_tenant_id, close_batch
from schema_ingester import get_tenant_id, get_class_id, get_mixin_id, get_schema_id

from get_token import get_access_token


LOGGER = setup_logger(__name__)


def ingest():
    """
    :return: None
    """
    # Read the configs
    with open("config.yaml", 'r') as ymlfile:
        cfg = yaml.safe_load(ymlfile)

    # Server parameters
    ims_host = cfg["Server"]["ims_host"]
    ims_endpoint_jwt = cfg["Server"]["ims_endpoint_jwt"]

    # Enterprise parameters used to construct JWT
    api_key = cfg["Enterprise"]["api_key"]
    org_id = cfg["Enterprise"]["org_id"]
    client_secret = cfg["Enterprise"]["client_secret"]
    tech_acct = cfg["Enterprise"][ "tech_acct"]
    priv_key_filename = cfg["Enterprise"]["priv_key_filename"]

    # read private key from file
    priv_key_file = open(priv_key_filename, "r")
    priv_key = priv_key_file.read()
    priv_key_file.close()

    # Get the platform url
    platform_gateway_url = cfg['Platform']['platform_gateway']

    # Get the IMS Token
    ims_token = "Bearer " + get_access_token(ims_host, ims_endpoint_jwt, org_id, tech_acct, api_key,
                                             client_secret, priv_key)


    # Get the titles for the class, mixin, schema and dataset
    class_title = cfg['Titles for Schema and Dataset']['class_title']
    mixin_title = cfg['Titles for Schema and Dataset']['mixin_title']
    schema_title = cfg['Titles for Schema and Dataset']['schema_title']
    dataset_title = cfg['Titles for Schema and Dataset']['dataset_title']
    file_with_tenant_id = cfg['Titles for Schema and Dataset']['file_with_tenant_id']

    # Construct the urls
    schema_registry_uri = "/data/foundation/schemaregistry/"
    tenant_id_url = platform_gateway_url + schema_registry_uri + "stats"
    create_class_url = platform_gateway_url + schema_registry_uri + "tenant/classes"
    create_mixin_url = platform_gateway_url + schema_registry_uri + "tenant/mixins"
    create_schema_url = platform_gateway_url + schema_registry_uri + "tenant/schemas"
    create_dataset_url = platform_gateway_url + "/data/foundation/catalog/datasets?requestDataSource=true"
    create_batch_url = platform_gateway_url + "/data/foundation/import/batches"

    # headers
    headers = {
        "Authorization": ims_token,
        "x-api-key": api_key,
        "x-gw-ims-org-id": org_id
    }

    data_for_class = cfg["Data for creating class"]
    data_for_mixin = cfg["Data for creating mixin"]
    data_for_schema = cfg["Data for creating schema"]

    try:
        tenant_id = get_tenant_id(tenant_id_url, headers)
        class_id = get_class_id(create_class_url, headers, class_title, data_for_class)
        mixin_id = get_mixin_id(create_mixin_url, headers, mixin_title, data_for_mixin, class_id, tenant_id)
        schema_id = get_schema_id(create_schema_url, headers, schema_title, class_id, mixin_id, data_for_schema)
        dataset_id = get_dataset_id(create_dataset_url, headers, dataset_title, schema_id)
        batch_id = get_batch_id(create_batch_url, headers, dataset_id)
        replace_tenant_id(file_with_tenant_id, tenant_id)
        upload_file(create_batch_url, headers, file_with_tenant_id, dataset_id, batch_id)
        close_batch(create_batch_url, headers, batch_id)

    except requests.exceptions.HTTPError as httperr:
        LOGGER.error('HTTPError Error: %s', httperr)

    except requests.exceptions.ConnectionError as connerr:
        LOGGER.error('ConnectionError Error: %s', connerr)

    except requests.exceptions.Timeout as touterr:
        LOGGER.error('Timeout Error: %s', touterr)

    except requests.exceptions.RequestException as rerr:
        LOGGER.error('Request Exception Error: %s', rerr)


if __name__ == "__main__":
    ingest()
