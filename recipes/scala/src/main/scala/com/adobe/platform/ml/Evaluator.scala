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

import java.util

import com.adobe.platform.ml.sdk.MLEvaluator
import com.adobe.platform.ml.sdk.MLMetric
import com.adobe.platform.ml.config.ConfigProperties
import org.apache.spark.ml.Transformer
import org.apache.spark.sql.DataFrame
import org.apache.spark.sql.functions._


class Evaluator extends MLEvaluator {

  override def split(configProperties:ConfigProperties, data: DataFrame): (DataFrame, DataFrame) = {
    val dataSplit = data.randomSplit(Array(0.8, 0.2), seed = 11L)
    (dataSplit(0), dataSplit(1))

  }

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
