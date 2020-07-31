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

import com.adobe.platform.ml.config.ConfigProperties
import com.adobe.platform.query.QSOption
import org.apache.spark.ml.feature.StringIndexer
import org.apache.spark.sql.expressions.Window
import org.apache.spark.sql.functions._
import org.apache.spark.sql.types.{StructType, TimestampType}
import org.apache.spark.sql.{DataFrame, SparkSession}
import org.apache.spark.sql.Column


class Helper {
  final val PLATFORM_SDK_PQS_PACKAGE: String = "com.adobe.platform.query"
  final val PLATFORM_SDK_PQS_INTERACTIVE: String = "interactive"
  final val PLATFORM_SDK_PQS_BATCH: String = "batch"

  /**
    *
    * @param configProperties - Configuration Properties map
    * @param sparkSession     - SparkSession
    * @return                 - DataFrame which is loaded for training
    */


  def load_dataset(configProperties: ConfigProperties, sparkSession: SparkSession, taskId: String): DataFrame = {

    require(configProperties != null)
    require(sparkSession != null)

    // Read the configs
    val serviceToken: String = sparkSession.sparkContext.getConf.get("ML_FRAMEWORK_IMS_ML_TOKEN", "").toString
    val userToken: String = sparkSession.sparkContext.getConf.get("ML_FRAMEWORK_IMS_TOKEN", "").toString
    val orgId: String = sparkSession.sparkContext.getConf.get("ML_FRAMEWORK_IMS_ORG_ID", "").toString
    val apiKey: String = sparkSession.sparkContext.getConf.get("ML_FRAMEWORK_IMS_CLIENT_ID", "").toString
    val sandboxName: String = sparkSession.sparkContext.getConf.get("sandboxName", "").toString

    val dataSetId: String = configProperties.get(taskId).getOrElse("")

    // Load the dataset
    var df = sparkSession.read.format(PLATFORM_SDK_PQS_PACKAGE)
      .option(QSOption.userToken, userToken)
      .option(QSOption.serviceToken, serviceToken)
      .option(QSOption.imsOrg, orgId)
      .option(QSOption.apiKey, apiKey)
      .option(QSOption.mode, PLATFORM_SDK_PQS_INTERACTIVE)
      .option(QSOption.datasetId, dataSetId)
      .option(QSOption.sandboxName, sandboxName)
      .load()
    df.show()
    df
  }

  /**
    *
    * @param configProperties - Configuration Properties map
    * @param dataframe        - DataFrame which needs to be prepared for training
    * @return                 - Dataframe which is ready for training
    */

  def prepare_dataset(configProperties: ConfigProperties,dataframe: DataFrame):DataFrame = {

    require(configProperties != null)
    require(dataframe != null)

    val timeframe: String = configProperties.get("timeframe").getOrElse("")
    val labelColumn: String = configProperties.get("evaluation.labelColumn").getOrElse("label")
    val scalingColumn: String = configProperties.get("evaluation.scalingColumn").getOrElse("scalingColumn")

    val sparkSession = dataframe.sparkSession
    import sparkSession.implicits._

    var df = dataframe.select(flattenSchema(dataframe.schema):_*)
    df = df.drop("_id").drop("eventType").drop("timestamp")
    df.printSchema()
    df.show()

    // Filter the data based on the config
    if(!timeframe.isEmpty) {
      val timeForFiltering = LocalDateTime.now().minusMinutes(timeframe.toLong)
        .toString.replace("T", " ")
      df = df.filter($"date".>=(timeForFiltering))
    } else df

    // Convert isHoliday to Int
    df = df.withColumn("isHoliday", $"isHoliday".cast("Int"))

    // Get the week and year from the date
    df = df.withColumn("date", unix_timestamp($"date", "MM/dd/yy").cast(TimestampType)).withColumn("week", weekofyear($"date")).withColumn("year", year($"date"))

    // Compute the weeklySalesAhead, weeklySalesLag, weeklySalesDiff
    val window = Window.partitionBy("store").orderBy("date")
    df = df.withColumn("weeklySalesLag", lag("weeklySales", 1).over(window)).filter(!isnull($"weeklySalesLag"))
    df = df.withColumn(labelColumn, lag("weeklySales", -1).over(window)).filter(!isnull(col(labelColumn)))
    df = df.withColumn(scalingColumn, lag(labelColumn, -1).over(window)).filter(!isnull(col(scalingColumn)))
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

    df
  }

  /**
    *
    * @param schema - schema of Struct Type to be flattened
    * @param prefix - prefix of String type
    * @return       - Array of type Column after flattening
    */

  def flattenSchema(schema: StructType, prefix: String = null) : Array[Column] = {
    schema.fields.flatMap(f => {
      val colName = if (prefix == null) f.name else (prefix + "." + f.name)

      f.dataType match {
        case st: StructType => flattenSchema(st, colName)
        case _ => Array(col(colName))
      }
    })
  }

}
