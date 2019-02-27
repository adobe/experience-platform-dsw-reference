/*#####################################################################
# ADOBE CONFIDENTIAL
# ___________________
#
#  Copyright 2018 Adobe
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
#####################################################################*/

package com.adobe.platform.ml

import java.time.LocalDateTime

import com.adobe.platform.dataset.DataSetOptions
import com.adobe.platform.ml.config.ConfigProperties
import com.adobe.platform.ml.sdk.DataLoader
import org.apache.spark.ml.feature.StringIndexer
import org.apache.spark.sql.expressions.Window
import org.apache.spark.sql.functions._
import org.apache.spark.sql.types.TimestampType
import org.apache.spark.sql.{DataFrame, SparkSession}

/**
  * Implementation of DataLoader which loads the dataframe and prepares the data
  */

class ScoringDataLoader extends DataLoader {

  /**
    *
    * @param configProperties - Configuration properties map
    * @param sparkSession     - SparkSession
    * @return                 - DataFrame which is prepared for scoring
    */

  override def load(configProperties: ConfigProperties, sparkSession: SparkSession): DataFrame = {

    require(configProperties != null)
    require(sparkSession != null)

    val serviceToken: String = sparkSession.sparkContext.getConf.get("ML_FRAMEWORK_IMS_ML_TOKEN", "").toString
    val userToken: String = sparkSession.sparkContext.getConf.get("ML_FRAMEWORK_IMS_TOKEN", "").toString
    val orgId: String = sparkSession.sparkContext.getConf.get("ML_FRAMEWORK_IMS_ORG_ID", "").toString
    val timeframe: String = configProperties.get("timeframe").getOrElse("")
    val dataSetId: String = configProperties.get("dataSetId").getOrElse("")
    val batchId: String = configProperties.get("batchId").getOrElse("")
    val apiKey:String = configProperties.get("apiKey").getOrElse("")

    var df = sparkSession.read.format("com.adobe.platform.dataset")
      .option(DataSetOptions.serviceToken, serviceToken)
      .option(DataSetOptions.userToken, userToken)
      .option(DataSetOptions.serviceApiKey, apiKey)
      .option(DataSetOptions.orgId, orgId)
      .option(DataSetOptions.batchId, batchId)
      .load(dataSetId)

    import sparkSession.implicits._

    // Convert isHoliday to Int
    df = df.withColumn("isHoliday", $"isHoliday".cast("Int"))

    // Get the week and year from the date
    df = df.withColumn("date", unix_timestamp($"date", "MM/dd/yy").cast(TimestampType)).withColumn("week", weekofyear($"date")).withColumn("year", year($"date"))

    // Compute the weeklySalesAhead, weeklySalesLag, weeklySalesDiff
    val window = Window.partitionBy("store").orderBy("date")
    df = df.withColumn("weeklySalesLag", lag("weeklySales", 1).over(window)).filter(!isnull($"weeklySalesLag"))
    df = df.withColumn("weeklySalesAhead", lag("weeklySales", -1).over(window)).filter(!isnull($"weeklySalesAhead"))
    df = df.withColumn("weeklySalesDiff", ($"weeklySales" - $"weeklySalesLag")/$"weeklySalesLag")

    // Convert the categorical data of storeType
    val indexer = new StringIndexer().setInputCol("storeType").setOutputCol("storeTypeIndex").fit(df)
    val indexed = indexer.transform(df)
    val categoriesIndicies = indexed.select("storeType","storeTypeIndex").distinct.rdd
    val categoriesMap = categoriesIndicies.map(x=>(x(0).toString,x(1).toString.toDouble)).collectAsMap

    def getCategoryIndex(catMap: scala.collection.Map[String,Double], expectedValue: Double) = udf((columnValue: String) =>
      if (catMap(columnValue) == expectedValue) 1 else 0)

    df = categoriesMap.keySet.toSeq.foldLeft[DataFrame](indexed)(
      (acc,c) =>
        acc.withColumn(c,getCategoryIndex(categoriesMap,categoriesMap(c))($"storeType"))
    )

    df = df.drop("storeTypeIndex")

    // Order by date and split the data
    df = df.orderBy("date").withColumn("date", $"date".cast("String"))
    if(!timeframe.isEmpty) {
      val timeForFiltering = LocalDateTime.now().minusMinutes(timeframe.toLong)
        .toString.replace("T", " ")
      df = df.filter($"date".>=(timeForFiltering))
    }
    else {
      df = df.filter($"date".>("2012-01-27 00:00:00"))
    }
    df
  }
}



