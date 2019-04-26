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



# Set up abstractEvaluator
abstractEvaluator <- evaluators.r::regressionEvaluator

#' applicationEvaluator
#'
#' @keywords applicationEvaluator
#' @export applicationEvaluator
#' @exportClass applicationEvaluator
applicationEvaluator <- setRefClass("applicationEvaluator",
  contains = "regressionEvaluator",
  methods = list(
    split = function(configurationJSON) {
      print("Running Split Function.")

      #########################################
      # Load Libraries
      #########################################
      library(gbm)
      library(lubridate)
      library(tidyverse)
      #########################################
      # Load Data
      #########################################
      reticulate::use_python("/usr/bin/python3.6")
      data_access_sdk_python <- reticulate::import("data_access_sdk_python")

      reader <- data_access_sdk_python$reader$DataSetReader(client_id = configurationJSON$ML_FRAMEWORK_IMS_USER_CLIENT_ID,
                                                            user_token = configurationJSON$ML_FRAMEWORK_IMS_TOKEN,
                                                            service_token = configurationJSON$ML_FRAMEWORK_IMS_ML_TOKEN)

      df <- reader$load(configurationJSON$trainingDataSetId, configurationJSON$ML_FRAMEWORK_IMS_ORG_ID)
      df <- as_tibble(df)

      #######################################
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
      
      traindf <- df %>%
        filter(if(!is.null(timeframe)) {
          date >= as.Date(Sys.time()-as.numeric(timeframe)*60) & date <= as.Date(Sys.time())
        } else {
          date >= "2010-02-12" & date <= "2012-01-27"  
        }) %>%
        select(-date)
      
      testdf <- df %>%
        filter(if(!is.null(timeframe)) {
          date >= as.Date(Sys.time()-as.numeric(timeframe)*60) & date <= as.Date(Sys.time())
        } else {
          date >= "2012-02-03"  
        }) %>%
        select(-date)
      
      return (list(train = traindf, test = testdf))
    }
  )
)