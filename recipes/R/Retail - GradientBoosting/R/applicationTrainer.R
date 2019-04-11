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
      # Load Data
      #########################################
      reticulate::use_python("/usr/bin/python3.6")
      data_access_sdk_python <- reticulate::import("data_access_sdk_python")
      
      reader <- data_access_sdk_python$reader$DataSetReader(client_id = configurationJSON$ML_FRAMEWORK_IMS_USER_CLIENT_ID,
                                                            user_token = configurationJSON$ML_FRAMEWORK_IMS_TOKEN,
                                                            service_token = configurationJSON$ML_FRAMEWORK_IMS_ML_TOKEN)
      
      df <- reader$load(configurationJSON$trainingDataSetId, configurationJSON$ML_FRAMEWORK_IMS_ORG_ID)
      df <- as_tibble(df)
      
      
      #########################################
      # Get hyperparameters
      #########################################
      learning_rate = if(!is.null(configurationJSON$learning_rate)) as.double(configurationJSON$learning_rate) else 0.1
      n_estimators = if(!is.null(configurationJSON$n_estimators)) as.integer(configurationJSON$n_estimators) else 100
      max_depth = if(!is.null(configurationJSON$max_depth)) as.integer(configurationJSON$max_depth) else 3
      
      
      #########################################
      # Data Preparation/Feature Engineering
      #########################################
      timeframe <- configurationJSON$timeframe
      if(any(names(df) == '_id')) {
        utils <- Utils$new()
        df = utils$removeTenantIdFromColumnNames(df)
      }
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
        filter(if(!is.null(timeframe)) {
        date >= as.Date(Sys.time()-as.numeric(timeframe)*60) & date <= as.Date(Sys.time())
        } else {
        date >= "2010-02-12" & date <= "2012-01-27"  
        }) %>%
        select(-date)
        print(nrow(df))


      #########################################
      # Build model and evaluate performance
      #########################################
      model <- gbm(weeklySalesAhead ~ ., data = df, distribution = "gaussian",
                   n.trees = n_estimators, interaction.depth = max_depth, 
                   shrinkage = learning_rate)
      
      
      #########################################
      # Save model to the chosen directory
      #########################################
      saveRDS(model, "model.rds")
      
      
      print("Exiting Trainer Function.")
    }
  )
)
