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
from dictor import dictor

from data_ingester import get_dataset_id, get_batch_id, upload_file, replace_tenant_id, close_batch
from schema_ingester import get_tenant_id, get_class_id, get_mixin_id, get_schema_id

from get_token import get_access_token


LOGGER = setup_logger(__name__)
TITLES = "Titles"
SERVER = "Server"
ENTERPRISE = "Enterprise"
PLATFORM = "Platform"
CLASS_DATA = "class_data"
INPUT_MIXIN_DATA = "input_mixin_data"
SCHEMA_DATA = "schema_data"
DATASET_DATA = "dataset_data"
BATCH_DATA = "batch_data"
OUTPUT_MIXIN_DATA = "output_mixin_data"


# Read the configs
with open("config.yaml", 'r') as ymlfile:
    cfg = yaml.safe_load(ymlfile)

    # Get the platform url
    platform_gateway_url = dictor(cfg, PLATFORM + ".platform_gateway", checknone=True)
    api_key = dictor(cfg, ENTERPRISE + ".api_key", checknone=True)
    org_id = dictor(cfg, ENTERPRISE + ".org_id", checknone=True)
    ims_token = dictor(cfg, PLATFORM + ".ims_token", checknone=True)

    if ims_token == "<ims_token>":
        # Server parameters
        ims_host = dictor(cfg, SERVER + ".ims_host", checknone=True)
        ims_endpoint_jwt = dictor(cfg, SERVER + ".ims_endpoint_jwt", checknone=True)

        # Enterprise parameters used to construct JWT
        client_secret = dictor(cfg, ENTERPRISE + ".client_secret", checknone=True)
        tech_acct = dictor(cfg, ENTERPRISE + ".tech_acct", checknone=True)
        priv_key_filename = dictor(cfg,  ENTERPRISE + ".priv_key_filename", checknone=True)

        # read private key from file
        priv_key_file = open(priv_key_filename, "r")
        priv_key = priv_key_file.read()
        priv_key_file.close()
        ims_token = "Bearer " + get_access_token(ims_host, ims_endpoint_jwt, org_id, tech_acct, api_key,
                                                 client_secret, priv_key)
    if not ims_token.startswith("Bearer "):
        ims_token = "Bearer " + ims_token

    # headers
    headers = {
        "Authorization": ims_token,
        "x-api-key": api_key,
        "x-gw-ims-org-id": org_id
    }


def ingest():
    """
    :return: None
    """
    # Get the titles for the class, mixin, schema and dataset
    input_class_title = dictor(cfg, TITLES + ".input_class_title", checknone=True)
    input_mixin_title = dictor(cfg, TITLES + ".input_mixin_title", checknone=True)
    input_mixin_definition_title = dictor(cfg, TITLES + ".input_mixin_definition_title", checknone=True)
    input_schema_title = dictor(cfg, TITLES + ".input_schema_title", checknone=True)
    input_dataset_title = dictor(cfg, TITLES + ".input_dataset_title", checknone=True)
    original_file = dictor(cfg, TITLES + ".file_replace_tenant_id", checknone=True)
    file_with_tenant_id = dictor(cfg, TITLES + ".file_with_tenant_id", checknone=True)
    is_output_schema_different = dictor(cfg,  TITLES + ".is_output_schema_different", checknone=True)
    output_mixin_title = dictor(cfg, TITLES + ".output_mixin_title", checknone=True)
    output_mixin_definition_title = dictor(cfg, TITLES + ".output_mixin_definition_title", checknone=True)
    output_schema_title = dictor(cfg, TITLES + ".output_schema_title", checknone=True)
    output_dataset_title = dictor(cfg, TITLES + ".output_dataset_title", checknone=True)

    # Construct the urls
    schema_registry_uri = "/data/foundation/schemaregistry/"
    tenant_id_url = platform_gateway_url + schema_registry_uri + "stats"
    create_class_url = platform_gateway_url + schema_registry_uri + "tenant/classes"
    create_mixin_url = platform_gateway_url + schema_registry_uri + "tenant/mixins"
    create_schema_url = platform_gateway_url + schema_registry_uri + "tenant/schemas"
    create_dataset_url = platform_gateway_url + "/data/foundation/catalog/datasets?requestDataSource=true"
    create_batch_url = platform_gateway_url + "/data/foundation/import/batches"

    data_for_class = dictor(cfg, CLASS_DATA, checknone=True)
    data_for_mixin = dictor(cfg, INPUT_MIXIN_DATA, checknone=True)
    data_for_schema = dictor(cfg, SCHEMA_DATA, checknone=True)
    data_for_dataset = dictor(cfg, DATASET_DATA, checknone=True)
    data_for_batch = dictor(cfg, BATCH_DATA, checknone=True)
    data_for_output_mixin = dictor(cfg, OUTPUT_MIXIN_DATA, checknone=True)

    try:
        tenant_id = get_tenant_id(tenant_id_url, headers)
        class_id = get_class_id(create_class_url, headers, input_class_title, data_for_class)
        input_mixin_id = get_mixin_id(create_mixin_url, headers, input_mixin_title, data_for_mixin, class_id,
                                      tenant_id, input_mixin_definition_title)
        input_schema_id = get_schema_id(create_schema_url, headers, input_schema_title, class_id, input_mixin_id, data_for_schema)
        input_dataset_id = get_dataset_id(create_dataset_url, headers, input_dataset_title, input_schema_id, data_for_dataset)
        batch_id = get_batch_id(create_batch_url, headers, input_dataset_id, data_for_batch)
        replace_tenant_id(original_file, file_with_tenant_id, tenant_id)
        upload_file(create_batch_url, headers, file_with_tenant_id, input_dataset_id, batch_id)
        close_batch(create_batch_url, headers, batch_id)
        if is_output_schema_different:
            output_mixin_id = get_mixin_id(create_mixin_url, headers, output_mixin_title, data_for_output_mixin,
                                           class_id, tenant_id, output_mixin_definition_title)
            output_schema_id = get_schema_id(create_schema_url, headers, output_schema_title, class_id, output_mixin_id,
                                         data_for_schema)
            get_dataset_id(create_dataset_url, headers, output_dataset_title, output_schema_id, data_for_dataset)

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
