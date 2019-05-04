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

import sys
import requests
from utils import setup_logger

from data_ingester import get_dataset_id, get_batch_id, upload_file, replace_tenant_id, close_batch
from schema_ingester import get_tenant_id, get_class_id, get_mixin_id, get_schema_id

from get_token import get_access_token

if sys.version_info[0] == 2:
    from ConfigParser import RawConfigParser
if sys.version_info[0] >= 3:
    from configparser import RawConfigParser

LOGGER = setup_logger(__name__)


def ingest():
    """
    :return: None
    """
    # Read the configs
    config = RawConfigParser()
    config_file_path = r'userconfig.config'
    config.read(config_file_path)

    # server parameters
    ims_host = config.get("server", "ims_host")
    ims_endpoint_jwt = config.get("server", "ims_endpoint_jwt")

    # enterprise parameters used to construct JWT
    api_key = config.get("enterprise", "api_key")
    org_id = config.get("enterprise", "org_id")
    client_secret = config.get("enterprise", "client_secret")
    tech_acct = config.get("enterprise", "tech_acct")
    priv_key_filename = config.get("enterprise", "priv_key_filename")

    # read private key from file
    priv_key_file = open(priv_key_filename, "r")
    priv_key = priv_key_file.read()
    priv_key_file.close()

    # Get the platform url
    platform_gateway_url = config.get('Platform', 'platform_gateway')

    # Get the IMS Token
    ims_token = "Bearer " + get_access_token(ims_host, ims_endpoint_jwt, org_id, tech_acct, api_key,
                                             client_secret, priv_key)


    # Get the titles for the class, mixin, schema and dataset
    class_title = config.get('Titles for Schema and Dataset', 'class_title')
    mixin_title = config.get('Titles for Schema and Dataset', 'mixin_title')
    schema_title = config.get('Titles for Schema and Dataset', 'schema_title')
    dataset_title = config.get('Titles for Schema and Dataset', 'dataset_title')
    file_with_tenant_id = config.get('Titles for Schema and Dataset', 'file_with_tenant_id')

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

    try:
        tenant_id = get_tenant_id(tenant_id_url, headers)
        class_id = get_class_id(create_class_url, headers, class_title)
        mixin_id = get_mixin_id(create_mixin_url, headers, mixin_title, class_id, tenant_id)
        schema_id = get_schema_id(create_schema_url, headers, schema_title, class_id, mixin_id)
       
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
