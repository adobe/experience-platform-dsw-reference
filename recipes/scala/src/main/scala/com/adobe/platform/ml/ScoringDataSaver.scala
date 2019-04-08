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

import com.adobe.platform.dataset.DataSetOptions
import com.adobe.platform.ml.config.ConfigProperties
import com.adobe.platform.ml.impl.Constants
import com.adobe.platform.ml.sdk.DataSaver
import org.apache.spark.sql.DataFrame

/**
  * Implementation of data saver which saves the output dataframe
  */
class ScoringDataSaver extends DataSaver {

  /**
    * Method that saves the scoring data into a dataframe
    * @param configProperties  - Configuration Properties map
    * @param dataFrame         - Dataframe with the scoring results
    */
  override def save(configProperties: ConfigProperties, dataFrame: DataFrame): Unit =  {

    require(configProperties != null)
    require(dataFrame != null)

    val predictionColumn = configProperties.get(Constants.PREDICTION_COL).getOrElse(Constants.DEFAULT_PREDICTION)
    val sparkSession = dataFrame.sparkSession

    val serviceToken: String = sparkSession.sparkContext.getConf.get("ML_FRAMEWORK_IMS_ML_TOKEN", "").toString
    val userToken: String = sparkSession.sparkContext.getConf.get("ML_FRAMEWORK_IMS_TOKEN", "").toString
    val orgId: String = sparkSession.sparkContext.getConf.get("ML_FRAMEWORK_IMS_ORG_ID", "").toString
    val apiKey:String = configProperties.get("apiKey").getOrElse("")

    val scoredDataSetId: String = configProperties.get("scoredDataSetId").getOrElse("")

    dataFrame.select(predictionColumn, "store", "date").write.format("com.adobe.platform.dataset")
      .option(DataSetOptions.orgId, orgId)
      .option(DataSetOptions.serviceToken, serviceToken)
      .option(DataSetOptions.userToken, userToken)
      .option(DataSetOptions.serviceApiKey, apiKey)
      .save(scoredDataSetId)

  }
}
