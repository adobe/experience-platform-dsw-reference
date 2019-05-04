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

from pyspark.sql.functions import col, avg, sqrt, abs, pow, lit


def split(configProperties, dataframe):

    # Order by date and split the data
    df = dataframe.orderBy("date").withColumn("date", col("date").cast("String"))
    train = df.filter(df["date"] <= lit('2012-01-27 00:00:00'))
    test = df.filter(df["date"] > lit('2012-01-27 00:00:00'))
    return train, test


def evaluate(dataframe, model, configProperties):
    df = model.transform(dataframe)
    df = df.withColumn("Diff", df["weeklySalesAhead"] - df["prediction"])
    df = df.withColumn("AbsValueOfDiff", abs(df.Diff))
    df = df.withColumn("forMAPE", df["AbsValueOfDiff"]/df["weeklySalesAhead"])

    mape = df.select(col("forMAPE")).rdd.flatMap(list).first()
    mae = df.select(avg("AbsValueOfDiff")).rdd.flatMap(list).first()
    rmse = df.select(sqrt(avg(pow(df.Diff, 2)))).rdd.flatMap(list).first()

    metric = [{"name": "MAPE", "value": mape, "valueType": "double"},
              {"name": "MAE", "value": mae, "valueType": "double"},
              {"name": "RMSE", "value": rmse, "valueType": "double"}]
    return metric