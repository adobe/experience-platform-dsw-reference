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


from pyspark.ml.feature import StringIndexer
from pyspark.sql.functions import col
from pyspark.sql.types import IntegerType
from pyspark.sql.functions import unix_timestamp, from_unixtime, to_date, lit, lag, udf, date_format
from pyspark.sql import Window
import datetime


def load_dataset(config_properties, spark, task_id):

    service_token = str(spark.sparkContext.getConf().get("ML_FRAMEWORK_IMS_ML_TOKEN"))
    user_token = str(spark.sparkContext.getConf().get("ML_FRAMEWORK_IMS_TOKEN"))
    org_id = str(spark.sparkContext.getConf().get("ML_FRAMEWORK_IMS_ORG_ID"))
    api_key = str(spark.sparkContext.getConf().get("ML_FRAMEWORK_IMS_CLIENT_ID"))
    sandbox_id = str(spark.sparkContext.getConf().get("sandboxId"))
    sandbox_name = str(spark.sparkContext.getConf().get("sandboxName"))

    dataset_id = str(config_properties.get(task_id))

    for arg in ['service_token', 'user_token', 'org_id', 'dataset_id', 'api_key']:
        if eval(arg) == 'None':
            raise ValueError("%s is empty" % arg)


    dataset_options = get_dataset_options(spark.sparkContext)

    #create map object
    creds = {}
    creds[dataset_options.serviceApiKey()] = api_key
    creds[dataset_options.serviceToken()] = service_token
    creds[dataset_options.userToken()] = user_token
    creds[dataset_options.orgId()] = org_id
    creds[dataset_options.sandboxName()] = sandbox_name
    creds[dataset_options.sandboxId()] = sandbox_id

    platform_sdk = get_platform_sdk(spark.sparkContext)
    resolver = platform_sdk.resolve()

    pd = spark.read.format(resolver.credentials(creds).resolveDataSetFormat(dataset_id)) \
         .options(creds) \
         .load(dataset_id)
    return pd


def prepare_dataset(config_properties, dataset):

    tenant_id = str(config_properties.get("tenant_id"))

    # Flatten the data
    if tenant_id in dataset.columns:
        dataset = dataset.select(col(tenant_id + ".*"))
        dataset.show()

    # Filter the data
    timeframe = str(config_properties.get("timeframe"))
    if timeframe != 'None':
        filterByTime = str(datetime.datetime.now() - datetime.timedelta(minutes=int(timeframe)))
        dataset = dataset.filter(dataset["date"] >= lit(str(filterByTime)))
        print("Number of rows after filtering : " + str(dataset.count()))

    # Convert isHoliday boolean value to Int
    pd = dataset.withColumn("isHoliday", col("isHoliday").cast(IntegerType()))

    # Get the week and year from date
    pd = pd.withColumn("week", date_format(to_date("date", "MM/dd/yy"), "w").cast(IntegerType()))
    pd = pd.withColumn("year", date_format(to_date("date", "MM/dd/yy"), "Y").cast(IntegerType()))

    # Convert the date to TimestampType
    pd = pd.withColumn("tx_date", to_date(unix_timestamp(pd["date"], "MM/dd/yy").cast("timestamp")))

    # Convert categorical data
    indexer = StringIndexer(inputCol="storeType", outputCol="storeTypeIndex")
    pd = indexer.fit(pd).transform(pd)

    # Get the WeeklySalesAhead and WeeklySalesLag column values
    window = Window.orderBy("tx_date").partitionBy("store")
    pd = pd.withColumn("weeklySalesLag", lag("weeklySales", 1).over(window)).na.drop(subset=["weeklySalesLag"])
    pd = pd.withColumn("weeklySalesAhead", lag("weeklySales", -1).over(window)).na.drop(subset=["weeklySalesAhead"])
    pd = pd.withColumn("weeklySalesScaled", lag("weeklySalesAhead", -1).over(window)).na.drop(subset=["weeklySalesScaled"])
    pd = pd.withColumn("weeklySalesDiff", (pd['weeklySales'] - pd['weeklySalesLag'])/pd['weeklySalesLag'])

    pd = pd.na.drop()
    return pd


def get_dataset_options(spark_context):
    dataset_options = spark_context._jvm.com.adobe.platform.dataset.DataSetOptions
    return dataset_options

#get platform-sdk
def get_platform_sdk(spark_context):
    platform_sdk = spark_context._jvm.com.adobe.platform.dataset.PlatformSDK
    return platform_sdk
