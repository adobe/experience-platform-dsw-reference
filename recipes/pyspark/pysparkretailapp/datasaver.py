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


def save(configProperties, prediction, sparkSession):

    if configProperties is None:
        raise ValueError("configProperties parameter is null")
    if prediction is None:
        raise ValueError("prediction parameter is null")
    if sparkSession is None:
        raise ValueError("sparkSession parameter is null")

    service_token = str(sparkSession.sparkContext.getConf().get("ML_FRAMEWORK_IMS_ML_TOKEN"))
    user_token = str(sparkSession.sparkContext.getConf().get("ML_FRAMEWORK_IMS_TOKEN"))
    org_id = str(sparkSession.sparkContext.getConf().get("ML_FRAMEWORK_IMS_ORG_ID"))

    scored_dataset_id = str(configProperties.get("scored_dataset_id"))
    api_key = str(configProperties.get("api_key"))

    for arg in ['service_token', 'user_token', 'org_id', 'scored_dataset_id', 'api_key']:
        if eval(arg) == 'None':
            raise ValueError("%s is empty" % arg)

    prediction.select("prediction", "store", "date").write.format("com.adobe.platform.dataset") \
        .option('orgId', org_id) \
        .option('serviceToken', service_token) \
        .option('userToken', user_token) \
        .option('serviceApiKey', api_key) \
        .save(scored_dataset_id)
