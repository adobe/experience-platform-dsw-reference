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
CONTENT_TYPE = "application/json"


def get_tenant_id(tenant_id_url, headers):
    """
    Get TenantId by making a GET call to "/data/foundation/schemaregistry/stats"
    :param tenant_id_url - url
    :param headers - headers
    :return - tenant id

    """
    res_text = http_request("get", tenant_id_url, headers)
    tenant_id = "_" + json.loads(res_text)["tenantId"]
    LOGGER.debug("tenant_id = %s", tenant_id)
    return tenant_id


def get_class_id(create_class_url, headers, class_title):
    """
    Get the classId by making a POST REQUEST to "/data/foundation/schemaregistry/tenant/classes"
    :param create_class_url:  url
    :param headers: headers
    :param class_title: class title
    :return: class url
    """

    data_for_create_class = {
        "type": "object",
        "title": class_title,
        "auditable": True,
        "meta:extends": [
            "https://ns.adobe.com/xdm/data/time-series"
        ],
        "description": class_title,
        "allOf": [
            {
                "$ref": "https://ns.adobe.com/xdm/data/time-series"
            }
        ]
    }
    headers["content-type"] = CONTENT_TYPE
    res_text = http_request("POST", create_class_url, headers, json.dumps(data_for_create_class))
    class_id = json.loads(res_text)["$id"]
    LOGGER.debug("class_id = %s", class_id)
    return class_id


def get_mixin_id(create_mixin_url, headers, mixin_title, class_id, tenant_id):
    """
    Get the mixinId by making a POST REQUEST to "/data/foundation/schemaregistry/tenant/mixins"

    :param create_mixin_url: url
    :param headers: headers
    :param mixin_title: mixin title
    :param class_id: class url
    :param tenant_id: tenant id in the org
    :return: mixin url
    """
    data_for_create_mixin = {
        "type": "object",
        "title": mixin_title,
        "description": mixin_title,
        "meta:intendedToExtend": [class_id],
        "definitions": {
            "retail": {
                "properties": {
                    tenant_id: {
                        "type": "object",
                        "properties": {
                            "date": {
                                "title": "date",
                                "type": "string",
                                "description": "date"
                            },
                            "store": {
                                "title": "store",
                                "type": "integer",
                                "description": "store"
                            },
                            "storeType": {
                                "title": "storeType",
                                "type": "string",
                                "description": "storeType"
                            },
                            "weeklySales": {
                                "title": "weeklySales",
                                "type": "number",
                                "description": "weeklySales"
                            },
                            "storeSize": {
                                "title": "storeSize",
                                "type": "integer",
                                "description": "storeSize"
                            },
                            "temperature": {
                                "title": "temperature",
                                "type": "number",
                                "description": "temperature"
                            },
                            "regionalFuelPrice": {
                                "title": "regionalFuelPrice",
                                "type": "number",
                                "description": "regionalFuelPrice"
                            },
                            "markdown": {
                                "title": "markdown",
                                "type": "number",
                                "description": "markdown"
                            },
                            "cpi": {
                                "title": "cpi",
                                "type": "number",
                                "description": "cpi"
                            },
                            "unemployment": {
                                "title": "unemployment",
                                "type": "number",
                                "description": "unemployment"
                            },
                            "isHoliday": {
                                "title": "isHoliday",
                                "type": "boolean",
                                "description": "isHoliday"
                            }
                        }
                    }
                }
            }
        },
        "allOf": [
            {
                "$ref": "#/definitions/retail"
            }
        ]
    }
    headers["content-type"] = CONTENT_TYPE
    res_text = http_request("post", create_mixin_url, headers, json.dumps(data_for_create_mixin))
    mixin_id = json.loads(res_text)["$id"]
    LOGGER.debug("mixin_id = %s", mixin_id)
    return mixin_id


def get_schema_id(create_schema_url, headers, schema_title, class_id, mixin_id):
    """
    Get the schemaId by making a POST REQUEST to "/data/foundation/schemaregistry/tenant/schemas"

    :param create_schema_url: url
    :param headers: headers
    :param schema_title: schema title
    :param class_id: class_url
    :param mixin_id: mixin_url
    :return: schema_url
    """
    data_for_create_schema = {
        "type": "object",
        "title": schema_title,
        "auditable": True,
        "meta:extends": [
            mixin_id,
            class_id
        ],
        "description": schema_title,
        "allOf": [
            {
                "$ref": mixin_id
            },
            {
                "$ref": class_id
            }
        ]
    }
    headers["Content-type"] = "application/json"
    res_text = http_request("post", create_schema_url, headers, json.dumps(data_for_create_schema))
    schema_id = json.loads(res_text)["$id"]
    LOGGER.debug("schema_id = %s", schema_id)
    return schema_id
