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

import java.util.UUID

import com.adobe.platform.ml.config.ConfigProperties
import com.adobe.platform.ml.sdk.DataSaver
import org.apache.spark.sql.DataFrame
import org.slf4j.LoggerFactory

/**
  * Implementation of data saver which saves the output dataframe to the output location
  * specified in the configuration file
  */
class ScoringDataSaver extends DataSaver {
  private val logger = LoggerFactory.getLogger(this.getClass)

  /**
    * Method that saves the scoring data into a dataframe
    * @param configProperties Properties map
    * @param dataFrame Dataframe with the scoring results
    */
  override def save(configProperties: ConfigProperties, dataFrame: DataFrame): Unit =  {

    val scoringResultsLocation: String = configProperties.get("scoringResultsLocation").get.toString

    val finalLocation: String = scoringResultsLocation + "/" + UUID.randomUUID()
    logger.info("*********************")
    logger.info(dataFrame.schema.toString)
    logger.info("Writing data to " + finalLocation)
    dataFrame.write.save(finalLocation)
    logger.info("*********************")
  }
}
