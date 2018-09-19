# ADOBE CONFIDENTIAL
# ___________________
# Copyright 2018 Adobe Systems Incorporated
# All Rights Reserved.
# NOTICE: All information contained herein is, and remains
# the property of Adobe Systems Incorporated and its suppliers,
# if any. The intellectual and technical concepts contained
# herein are proprietary to Adobe Systems Incorporated and its
# suppliers and are protected by all applicable intellectual property
# laws, including trade secret and copyright laws.
# Dissemination of this information or reproduction of this material
# is strictly forbidden unless prior written permission is obtained
# from Adobe Systems Incorporated.



# Set up abstractScorer
abstractScorer <- ml.runtime.r::abstractScorer()

#' applicationScorer
#'
#' @keywords applicationScorer
#' @export applicationScorer
#' @exportClass applicationScorer
applicationScorer <- setRefClass("applicationScorer",
  contains = "abstractScorer",
  methods = list(
    score = function(configurationJSON) {
      print("Running Scorer Function.")

      # Set working directory to AZ_BATCHAI_INPUT_MODEL
      setwd(configurationJSON$modelPATH)


      #########################################
      # Load Libraries
      #########################################
      library(gbm)
      library(lubridate)
      library(tidyverse)
      set.seed(1234)


      #########################################
      # Extract fields from configProperties
      #########################################
      reticulate::use_python("/usr/bin/python3.6")

      data_access_sdk_python <- reticulate::import("data_access_sdk_python")

      reader <- data_access_sdk_python$reader$DataSetReader(client_id = configurationJSON$ML_FRAMEWORK_IMS_USER_CLIENT_ID, user_token = configurationJSON$ML_FRAMEWORK_IMS_TOKEN, service_token = configurationJSON$ML_FRAMEWORK_IMS_ML_TOKEN)

      data <- reader$load(configurationJSON$scoringDataSetId, configurationJSON$ML_FRAMEWORK_IMS_ORG_ID)


      #########################################
      # Load Data
      #########################################
      df <- as_tibble(data)


      #########################################
      # Data Preparation/Feature Engineering
      #########################################
      df <- df %>%
        mutate(store = as.numeric(store)) %>%
        mutate(date = mdy(date), week = week(date), year = year(date)) %>%
        mutate(new = 1) %>%
        spread(storeType, new, fill = 0) %>%
        mutate(isHoliday = as.integer(isHoliday)) %>%
        mutate(weeklySalesAhead = lead(weeklySales, 45),
           weeklySalesLag = lag(weeklySales, 45),
           weeklySalesDiff = (weeklySales - weeklySalesLag) / weeklySalesLag) %>%
        drop_na() %>%
        select(-date)



      #########################################
      # Retrieve saved model from trainer
      #########################################
      retrieved_model <- readRDS("model.rds")


      #########################################
      # Evaluate Performance
      #########################################
      pred <- predict(retrieved_model, df, n.trees = 10000)
      mape <- mean(abs((test$weeklySalesAhead -  pred) / test$weeklySalesAhead))
      print(paste("Test Set MAPE: ", mape, sep = ""))
      print("Predictions:")
      print(pred)

      print("Exiting Scorer Function.")
    }
  )
)
