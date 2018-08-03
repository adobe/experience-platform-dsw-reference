/*
 *  Copyright 2017 Adobe.
 *
 *  Licensed under the Apache License, Version 2.0 (the "License");
 *  you may not use this file except in compliance with the License.
 *  You may obtain a copy of the License at
 *
 *          http://www.apache.org/licenses/LICENSE-2.0
 *
 *  Unless required by applicable law or agreed to in writing, software
 *  distributed under the License is distributed on an "AS IS" BASIS,
 *  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *  See the License for the specific language governing permissions and
 *  limitations under the License.
 */
package com.adobe.platform.ml

import com.adobe.platform.ml.config.ConfigProperties
import com.adobe.platform.ml.sdk.EvaluationProvider
import org.apache.spark.ml.evaluation.{BinaryClassificationEvaluator, Evaluator}
import org.apache.spark.sql.{DataFrame, SparkSession}
import org.slf4j.LoggerFactory

class SentimentEvaluatorProvider extends EvaluationProvider{

  private val logger = LoggerFactory.getLogger(this.getClass)

  override def getMetricsEvaluator(configProperties: ConfigProperties, sparkSession: SparkSession):
  Evaluator = new BinaryClassificationEvaluator()

  override def split(configProperties: ConfigProperties, sparkSession: SparkSession, trainingDF: DataFrame):
  (DataFrame, DataFrame) = {val splits = trainingDF.randomSplit(Array(0.8, 0.2), seed = 11L)
    (splits(0),splits(1))}

  override def saveEvaluationResult(configProperties: ConfigProperties, sparkSession: SparkSession,
                                    metricName: String, metricValue: Double): Unit =
    print(metricName+" for sentiment analysis is {}"+ metricValue.toString())
}
