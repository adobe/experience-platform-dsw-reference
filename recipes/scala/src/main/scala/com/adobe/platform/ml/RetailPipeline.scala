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

import com.adobe.platform.ml.config.ConfigProperties
import com.adobe.platform.ml.impl.Constants
import com.adobe.platform.ml.sdk.PipelineFactory
import org.apache.spark.ml.Pipeline
import org.apache.spark.ml.feature.VectorAssembler
import org.apache.spark.ml.param.ParamMap
import org.apache.spark.ml.regression.GBTRegressor
import org.apache.spark.sql.SparkSession

/**
  * Implementation of pipeline factory to configure the pipeline
  */


class RetailPipeline extends PipelineFactory {

    /**
      * @param configProperties  - Configuration Properties map from the pipelineservice.json
      * @return                  - Pipeline
      */

    override def apply(configProperties: ConfigProperties) = {

      require(configProperties != null)

      var inputFeatures: String = configProperties.get("ACP_DSW_INPUT_FEATURES").get.toString
      val tenantId:String = configProperties.get("tenantId").getOrElse("")
      val learning_rate : Float = configProperties.get("learning_rate").get.toFloat
      val n_estimators : Int = configProperties.get("n_estimators").get.toInt
      val max_depth : Int = configProperties.get("max_depth").get.toInt

      if(inputFeatures.startsWith(tenantId)) {
        inputFeatures = inputFeatures.replaceAll(tenantId + ".", "")
      }

      val featureList = inputFeatures.split(",").toList

      val itemsToRemove = List(Constants.LABEL_COL, "date", "storeType")

      val newFeatureList = featureList diff itemsToRemove

      val cols: Array[String] = newFeatureList.toArray

      val labelColumn = configProperties.get(Constants.LABEL_COL).getOrElse(Constants.DEFAULT_LABEL)
      val predictionColumn = configProperties.get(Constants.PREDICTION_COL).getOrElse(Constants.DEFAULT_PREDICTION)
      // Gradient-boosted tree estimator
      val gbt = new GBTRegressor()
        .setLabelCol(labelColumn)
        .setFeaturesCol("features")
        .setPredictionCol(predictionColumn)
        .setMaxDepth(max_depth)
        .setMaxBins(n_estimators)
        .setStepSize(learning_rate)

      // Assemble the fields to a vector
      val assembler = new VectorAssembler().setInputCols(cols).setOutputCol("features")
      //Define the Array with the stages of the pipeline
      val stages = Array(assembler,gbt)

      //Construct the pipeline
      val pipeline = new Pipeline().setStages(stages)

      pipeline
    }

  /***
    * Ability to add paramMap just before calling transform for your pipeline
    * @param configProperties - Configration Properties map
    * @param sparkSession     - SparkSession
    * @return                 - ParamMap
    */
    override def getParamMap(configProperties: ConfigProperties, sparkSession: SparkSession) : ParamMap = {
      val map = new ParamMap()
      map
    }
}
