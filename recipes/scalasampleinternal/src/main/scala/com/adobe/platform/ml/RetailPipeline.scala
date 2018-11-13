/** ***********************************************************************
  * ADOBE CONFIDENTIAL
  * ___________________
  *
  * Copyright 2017 Adobe Systems Incorporated
  * All Rights Reserved.
  *
  * NOTICE:  All information contained herein is, and remains
  * the property of Adobe Systems Incorporated and its suppliers,
  * if any.  The intellectual and technical concepts contained
  * herein are proprietary to Adobe Systems Incorporated and its
  * suppliers and are protected by all applicable intellectual property
  * laws, including trade secret and copyright laws.
  * Dissemination of this information or reproduction of this material
  * is strictly forbidden unless prior written permission is obtained
  * from Adobe Systems Incorporated.
  * *************************************************************************/
package com.adobe.platform.ml

import com.adobe.platform.ml.config.ConfigProperties
import com.adobe.platform.ml.sdk.PipelineFactory
import org.apache.spark.ml.Pipeline
import org.apache.spark.ml.classification.GBTClassifier
import org.apache.spark.ml.param.ParamMap
import org.apache.spark.sql.SparkSession


class RetailPipeline extends PipelineFactory {

    /**
      * Implementation of pipeline factory to configure the pipeline
      * @param configProperties Properties map from the pipelineservice.json
      * @return
      */
    override def apply(configProperties: ConfigProperties) = {

      val learning_rate : Float = configProperties.get("learning_rate").get.toFloat
      val n_estimators : Int  = configProperties.get("n_estimators").get.toInt
      val max_depth : Int  = configProperties.get("max_depth").get.toInt


      val gbt = new GBTClassifier()
        .setPredictionCol("weeklySalesAhead")
        .setMaxDepth(max_depth)
        .setMaxBins(n_estimators)
        .setStepSize(learning_rate)

      val pipeline = new Pipeline()
        .setStages(Array(gbt))

      pipeline
    }

  /***
    * Ability to add paramMap just before calling transform for your pipeline
    * @param configProperties
    * @param sparkSession
    * @return
    */
    override def getParamMap(configProperties: ConfigProperties, sparkSession: SparkSession) = {
      val map = new ParamMap()
      map
    }
}
