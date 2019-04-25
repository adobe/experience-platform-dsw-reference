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
import com.adobe.platform.ml.sdk.DataLoader
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

    val helper:Helper = new Helper()
    var df = helper.load_dataset(configProperties, sparkSession, "scoringDataSetId")
    df = helper.prepare_dataset(configProperties, df)
    df
  }
}



