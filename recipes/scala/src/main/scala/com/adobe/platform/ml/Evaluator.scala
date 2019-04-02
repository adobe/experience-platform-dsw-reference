/*#####################################################################
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
#####################################################################*/

package com.adobe.platform.ml

import java.util

import com.adobe.platform.ml.sdk.MLEvaluator
import com.adobe.platform.ml.sdk.MLMetric
import com.adobe.platform.ml.config.ConfigProperties
import org.apache.spark.ml.Transformer
import org.apache.spark.sql.{DataFrame, SparkSession}
import org.apache.spark.sql.functions._
import org.apache.spark.sql.types.TimestampType

/**
  * Implementation of Evaluator which splits the dataframe and evaluates it
  */

class Evaluator extends MLEvaluator {

  /**
    *
    * @param configProperties - Configuration Properties map
    * @param data             - DataFrame that is used to split the data
    * @return                 - Tuple of the dataframes
    */

  override def split(configProperties:ConfigProperties, data: DataFrame): (DataFrame, DataFrame) = {

    val sparkSession = data.sparkSession
    import sparkSession.implicits._

    // Order by date and split the data
    var df = data.orderBy("date").withColumn("date", $"date".cast("String"))
    var train_data = df.filter($"date".<=("2012-02-10 00:00:00"))
    var test_data = df.filter($"date".>("2012-01-27 00:00:00"))
    (train_data, test_data)
  }

  /**
    *
    * @param configProperties - Configuration Properties map
    * @param model            - Trained model to be used for evaluation
    * @param dataFrame        - DataFrame on which scoring and evaluations are made
    * @return                 - Arraylist of metrics
    */

  def evaluate(configProperties: ConfigProperties, model: Transformer, dataFrame: DataFrame): util.ArrayList[MLMetric] = {
    
    val sparkSession = dataFrame.sparkSession
    import sparkSession.implicits._

    var df = model.transform(dataFrame)

    df = df.withColumn("Diff", $"weeklySalesAhead" - $"prediction")
    df = df.withColumn("AbsValueOfDiff", abs($"weeklySalesAhead" - $"prediction"))
    df = df.withColumn("forMAPE", $"AbsValueOfDiff"/$"weeklySalesAhead")

    val mape = df.select(avg("forMAPE")).first.getDouble(0).toString()
    val mae = df.select(avg("AbsValueOfDiff")).first.getDouble(0).toString()
    val rmse = df.select(sqrt(avg(pow("Diff", 2)))).first.getDouble(0).toString()

    val metrics = new util.ArrayList[MLMetric]()
    metrics.add(new MLMetric("MAPE", mape, "double"))
    metrics.add(new MLMetric("MAE", mae,  "double"))
    metrics.add(new MLMetric("RMSE", rmse,  "double"))

    metrics

  }

}
