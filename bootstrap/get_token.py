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

import sys
import json
import datetime
import jwt

from utils import setup_logger, http_request

if sys.version_info[0] == 2:
    from urllib import urlencode

if sys.version_info[0] >= 3:
    from urllib.parse import urlencode


LOGGER = setup_logger(__name__)


def get_jwt_token(ims_host, org_id, tech_acct, api_key, priv_key):
    """

    :param ims_host: ims host
    :param org_id: org id
    :param tech_acct: technical account ID (obtained from Adobe IO integration)
    :param api_key: api key (obtained from Adobe IO integration)
    :param priv_key: private key counter part to the public key which was used for creating Adobe IO integration
    :return: encoded jwt token
    """

    # create payload
    payload = {
        "exp": token_expiration_millis(),
        "iss": org_id,
        "sub": tech_acct,
        "https://" + ims_host + "/s/" + "ent_dataservices_sdk": True,
        "aud": "https://" + ims_host + "/c/" + api_key
    }

    # create JSON Web Token
    jwt_token = jwt.encode(payload, priv_key, algorithm='RS256')

    LOGGER.debug("encoded jwt_token = %s", jwt_token)
    return jwt_token


def get_access_token(ims_host, ims_endpoint_jwt, org_id, tech_acct, api_key,
                     client_secret, priv_key):
    """

    :param ims_host: ims host
    :param ims_endpoint_jwt: endpoint for exchange jwt
    :param org_id: org id
    :param tech_acct: technical account ID (obtained from Adobe IO integration)
    :param api_key: api key (obtained from Adobe IO integration)
    :param client_secret: client secret (obtained from Adobe IO integration)
    :param priv_key : private key
    :return: access token for the apis
    """
    url = "https://" + ims_host + ims_endpoint_jwt

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Cache-Control": "no-cache"
    }

    body_credentials = {
        "client_id"     : api_key,
        "client_secret" : client_secret,
        "jwt_token"     : get_jwt_token(ims_host, org_id, tech_acct, api_key, priv_key)
    }
    body = urlencode(body_credentials)

    # send http post request
    res_text = http_request("post", url, headers, body)
    access_token = json.loads(res_text)["access_token"]
    LOGGER.debug("access_token: %s", access_token)
    return access_token


def token_expiration_millis():
    """
    :return: token expiration in milli seconds
    """
    dt = datetime.datetime.now()
    dt_str = dt.strftime('%s.%%06d') % dt.microsecond
    return int(float(dt_str)) + 24 * 60 * 60 * 1000
