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

import logging
import requests


def setup_logger(name):
    """
    :param name: name
    :return: logger
    """
    # create logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # create console handler and set level to debug
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    # create formatter
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s: %(message)s')

    # add formatter to console_handler
    console_handler.setFormatter(formatter)

    # add console_handler to logger
    logger.addHandler(console_handler)

    return logger


def http_request(method, url, headers, data=None):
    """
    Request util
    :param method: GET or POST or PUT
    :param url: url
    :param headers: headers
    :param data: optional data (needed for POST)
    :return: response text
    """
    response = requests.request(method, url, headers=headers, data=data)
    if response.status_code not in [200, 201]:
        http_error_msg = u'%s HTTP request failed: %s for url: %s' % (response.status_code, response.text, url)
        raise requests.exceptions.HTTPError(http_error_msg)
    return response.text

