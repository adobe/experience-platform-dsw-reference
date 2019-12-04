#####################################################################
# ADOBE CONFIDENTIAL
# ___________________
#
#  Copyright 2019 Adobe
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

from platform_sdk.client_context import ClientContext

def get_client_context(config_properties):
    for k, v in config_properties.items():
        print(k, v)
    return ClientContext(api_key=config_properties['ML_FRAMEWORK_IMS_USER_CLIENT_ID'],
                         org_id=config_properties['ML_FRAMEWORK_IMS_ORG_ID'],
                         user_token=config_properties['ML_FRAMEWORK_IMS_TOKEN'],
                         service_token=config_properties['ML_FRAMEWORK_IMS_ML_TOKEN'],
                         sandbox_id=config_properties['sandboxId'],
                         sandbox_name=config_properties['sandboxName'])

