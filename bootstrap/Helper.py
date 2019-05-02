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
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # create formatter
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s: %(message)s')

    # add formatter to ch
    ch.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(ch)

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







