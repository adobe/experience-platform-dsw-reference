# ADOBE CONFIDENTIAL
# ___________________
# Copyright 2019 Adobe Systems Incorporated
# All Rights Reserved.
# NOTICE: All information contained herein is, and remains
# the property of Adobe Systems Incorporated and its suppliers,
# if any. The intellectual and technical concepts contained
# herein are proprietary to Adobe Systems Incorporated and its
# suppliers and are protected by all applicable intellectual property
# laws, including trade secret and copyright laws.
# Dissemination of this information or reproduction of this material
# is strictly forbidden unless prior written permission is obtained
# from Adobe Systems Incorporated.

Helper <- setRefClass(
  Class = "Helper",
  methods = list(
    get_client_context = function(configurationJSON) {
      print("Getting Client Context.")
      
      reticulate::use_python("/usr/bin/python3.6")
      platform_sdk_python <- reticulate::import("platform_sdk")
      
      return (platform_sdk_python$client_context$ClientContext(api_key = configurationJSON$ML_FRAMEWORK_IMS_USER_CLIENT_ID,
                                                               org_id = configurationJSON$ML_FRAMEWORK_IMS_ORG_ID,
                                                               service_token = configurationJSON$ML_FRAMEWORK_IMS_ML_TOKEN,
                                                               user_token = configurationJSON$ML_FRAMEWORK_IMS_TOKEN,
                                                               sandbox_id = configurationJSON$sandboxId,
                                                               sandbox_name = configurationJSON$sandboxName))
    }
  )
)