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

    // val scoringResultsLocation: String = configProperties.get("scoringResultsLocation").get.toString

    // val finalLocation: String = scoringResultsLocation + "/" + UUID.randomUUID()
    logger.info("*********************")
    logger.info(dataFrame.schema.toString)
    // logger.info("Writing data to " + finalLocation)
    // dataFrame.write.save(finalLocation)
    logger.info("*********************")
  }
}
