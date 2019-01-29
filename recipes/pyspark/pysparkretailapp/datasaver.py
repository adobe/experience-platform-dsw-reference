#####################################################################
# ADOBE CONFIDENTIAL
# ___________________
#
#  Copyright 2017 Adobe
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


def save(configProperties, prediction):
    print("In save")
    print("Count is " + str(prediction.count()))
    print(" dataframe is")
    prediction.show()
    #print("The config Properties are ")
    #for key in configProperties.keys():
        #for value in configProperties[key]:
            #print(key, value)


    # spark = prediction.sparkContext

    # service_token = str(spark.getConf().get("ML_FRAMEWORK_IMS_ML_TOKEN"))
    # user_token = str(spark.getConf().get("ML_FRAMEWORK_IMS_TOKEN"))
    # org_id = str(spark.getConf().get("ML_FRAMEWORK_IMS_ORG_ID"))


    # This returns None for all the three values
    service_token = str(configProperties.get("ML_FRAMEWORK_IMS_ML_TOKEN"))
    user_token = str(configProperties.get("ML_FRAMEWORK_IMS_TOKEN"))
    org_id = str(configProperties.get("ML_FRAMEWORK_IMS_ORG_ID"))

    # print(service_token, user_token, org_id)

    scored_dataset_id = str(configProperties.get("scored_dataset_id"))
    api_key = str(configProperties.get("api_key"))

    prediction.select("prediction", "store", "date").write.format("com.adobe.platform.dataset") \
        .option('orgId', org_id) \
        .option('serviceToken', service_token) \
        .option('userToken', user_token) \
        .option('serviceApiKey', api_key) \
        .save(scored_dataset_id)

