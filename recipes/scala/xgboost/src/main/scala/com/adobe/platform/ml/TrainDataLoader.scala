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
import com.adobe.platform.ml.sdk.DataLoader
import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.types._

/**
  * Loader class for training data
  */
class TrainDataLoader extends DataLoader {

  /**
    * Method that loads the training data into a dataframe using sparksession
    * @param configProperties Properties map
    * @param sparkSession spark session
    * @return
    */
  override def load(configProperties: ConfigProperties, sparkSession: SparkSession) = {
    val trainingDataLocation: String = configProperties.get("trainingDataLocation").get.toString
    val sqlContext = new org.apache.spark.sql.SQLContext(sparkSession.sparkContext)
    val trainDF = sqlContext.read.format("libsvm").load(trainingDataLocation)
    trainDF
  }
}
