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
      # Load Data
      #########################################
      reticulate::use_python("/usr/bin/python3.6")

      data_access_sdk_python <- reticulate::import("data_access_sdk_python")

      reader <- data_access_sdk_python$reader$DataSetReader(client_id = configurationJSON$ML_FRAMEWORK_IMS_USER_CLIENT_ID, 
                                                            user_token = configurationJSON$ML_FRAMEWORK_IMS_TOKEN, 
                                                            service_token = configurationJSON$ML_FRAMEWORK_IMS_ML_TOKEN)

      df <- reader$load(configurationJSON$scoringDataSetId, configurationJSON$ML_FRAMEWORK_IMS_ORG_ID)
      df <- as_tibble(df)


      #########################################
      # Data Preparation/Feature Engineering
      #########################################
      timeframe <- configurationJSON$timeframe
      tenantId <- configurationJSON$tenantId
      if(!is.null(tenantId)){
        if(any(names(df) == '_id')) {
          #Drop id, eventType, timestamp and rename columns
          df <- df[,-c(1,2,3)]
          names(df) <- substring(names(df), nchar(tenantId)+2)
        }
      }
      df <- df %>%
        mutate(store = as.numeric(store)) %>%
        mutate(date = mdy(date), week = week(date), year = year(date)) %>%
        mutate(new = 1) %>%
        spread(storeType, new, fill = 0) %>%
        mutate(isHoliday = as.integer(isHoliday)) %>%
        mutate(weeklySalesAhead = lead(weeklySales, 45),
               weeklySalesLag = lag(weeklySales, 45),
               weeklySalesScaled = lead(weeklySalesAhead, 45),
               weeklySalesDiff = (weeklySales - weeklySalesLag) / weeklySalesLag) %>%
        drop_na() 
      
      test_df <- df %>%
        filter(if(!is.null(timeframe)) {
        date >= as.Date(Sys.time()-as.numeric(timeframe)*60) & date <= as.Date(Sys.time())
        } else {
        date >= "2010-02-12"  
        }) %>%
        select(-date)
        print(nrow(df))


      #########################################
      # Retrieve saved model from trainer
      #########################################
      retrieved_model <- readRDS("model.rds")


      #########################################
      # Generate Predictions
      #########################################
      pred <- predict(retrieved_model, test_df, n.trees = retrieved_model$n.trees)

      output_df <- df %>% 
        select(date, store) %>% 
        mutate(prediction = pred,
               store = as.integer(store),
               date = as.character(date))

      tenantId = configurationJSON$tenantId
      colnames(output_df) <- paste(tenantId, colnames(output_df), sep = ".")
      output_df[c("_id","eventType","timestamp")] = ""
      output_df$timestamp = "2019-01-01T00:00:00"

      
      #########################################
      # Write Results
      #########################################
      reticulate::use_python("/usr/bin/python3.6")
      data_access_sdk_python <- reticulate::import("data_access_sdk_python")

      print("Set up writer")
      writer <- data_access_sdk_python$writer$DataSetWriter(client_id = configurationJSON$ML_FRAMEWORK_IMS_USER_CLIENT_ID,
                                                            user_token = configurationJSON$ML_FRAMEWORK_IMS_TOKEN,
                                                            service_token = configurationJSON$ML_FRAMEWORK_IMS_ML_TOKEN)
      print("Writer configured")
      
      writer$write(data_set_id = configurationJSON$scoringResultsDataSetId,
                   dataframe = output_df,
                   ims_org = configurationJSON$ML_FRAMEWORK_IMS_ORG_ID,
                   file_format='json')
      print("Write done")
      
      
      print("Exiting Scorer Function.")
    }
  )
)
