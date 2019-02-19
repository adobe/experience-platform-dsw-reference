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


def load(configProperties, spark):

    if(configProperties is  None) :
        raise ValueError("configProperties parameter is null")
    if(spark is None):
        raise ValueError("spark parameter is null")

    service_token = str(spark.sparkContext.getConf().get("ML_FRAMEWORK_IMS_ML_TOKEN"))
    user_token = str(spark.sparkContext.getConf().get("ML_FRAMEWORK_IMS_TOKEN"))
    org_id = str(spark.sparkContext.getConf().get("ML_FRAMEWORK_IMS_ORG_ID"))

    dataset_id = str(configProperties.get("trainingDataSetId"))
    api_key = str(configProperties.get("api_key"))

    for arg in ['service_token', 'user_token', 'org_id', 'dataset_id', 'api_key']:
        if eval(arg) == 'None':
            raise ValueError("%s is empty" % arg)

    pd = spark.read.format("com.adobe.platform.dataset") \
        .option('serviceToken', service_token) \
        .option('userToken', user_token) \
        .option('orgId', org_id) \
        .option('serviceApiKey', api_key) \
        .load(dataset_id)

    # Convert isHoliday boolean value to Int
    pd = pd.withColumn("isHoliday", col("isHoliday").cast(IntegerType()))

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
    pd = pd.withColumn("weeklySalesDiff", (pd['weeklySales'] - pd['weeklySalesLag'])/pd['weeklySalesLag'])

    pd = pd.na.drop()

    # Split the data
    train = pd.filter(pd["tx_date"] <= lit('2012-01-27'))

    return train
