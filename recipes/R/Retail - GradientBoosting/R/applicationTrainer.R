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



# Set up abstractTrainer
abstractTrainer <- ml.runtime.r::abstractTrainer

#' applicationTrainer
#'
#' @keywords applicationTrainer
#' @export applicationTrainer
#' @exportClass applicationTrainer
applicationTrainer <- setRefClass("applicationTrainer",
  contains = "abstractTrainer",
  methods = list(
    train = function(configurationJSON) {
      print("Running Trainer Function.")

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
      
      reader <- data_access_sdk_python$reader$DataSetReader(user_token = customerConfigs$ML_FRAMEWORK_IMS_ML_TOKEN, service_token = customerConfigs$ML_FRAMEWORK_IMS_TOKEN)
      
      data <- reader$load(configurationJSON$dataSetId, configurationJSON$ML_FRAMEWORK_IMS_ORG_ID)
      #data = configurationJSON$data
      train_start = configurationJSON$train_start
      train_end = configurationJSON$train_end


      #########################################
      # Load Data
      #########################################
      df <- as_tibble(read.csv(data))


      #########################################
      # Data Preparation/Feature Engineering
      #########################################
      df <- df %>%
        mutate(date = mdy(date), week = week(date), year = year(date)) %>%
        mutate(new = 1) %>%
        spread(storeType, new, fill = 0) %>%
        mutate(isHoliday = as.integer(isHoliday)) %>%
        mutate(weeklySalesAhead = lead(weeklySales, 45),
           weeklySalesLag = lag(weeklySales, 45),
           weeklySalesDiff = (weeklySales - weeklySalesLag) / weeklySalesLag) %>%
        drop_na()

      train <- df %>%
        filter(date >= train_start & date <= train_end) %>%
        select(-date)


      #########################################
      # Build model and evaluate performance
      #########################################
      model <- gbm(weeklySalesAhead ~ ., data = train, distribution = "gaussian",
             n.trees = 10000, interaction.depth = 4)


      #########################################
      # Save model to the chosen directory
      #########################################
      saveRDS(model, "model.rds")

      print("Exiting Trainer Function.")
    }
  )
)
