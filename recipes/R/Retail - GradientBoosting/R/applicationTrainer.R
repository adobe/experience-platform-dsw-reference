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
    train = function(configurationJSON, df) {
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
      # Get hyperparameters
      #########################################
      learning_rate = if(!is.null(configurationJSON$learning_rate)) as.double(configurationJSON$learning_rate) else 0.1
      n_estimators = if(!is.null(configurationJSON$n_estimators)) as.integer(configurationJSON$n_estimators) else 100
      max_depth = if(!is.null(configurationJSON$max_depth)) as.integer(configurationJSON$max_depth) else 3

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
