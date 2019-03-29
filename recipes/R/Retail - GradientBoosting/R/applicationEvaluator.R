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
defaultRegressionEvaluator <- ml.runtime.r::defaultRegressionEvaluator

#' applicationEvaluator
#'
#' @keywords applicationEvaluator
#' @export applicationEvaluator
#' @exportClass applicationEvaluator
applicationEvaluator <- setRefClass("applicationEvaluator",
  contains = "defaultRegressionEvaluator",
  methods = list(
    split = function(df, configurationJSON) {
      print("Running Split Function.")

      #########################################
      # Split Data
      #########################################
      seed = 101
      if(!is.null(configurationJSON$evaluation.seed)){
      seed = as.numeric(configurationJSON$evaluation.seed)
      }
      trainRatio = 0.8
      if(!is.null(configurationJSON$evaluation.trainRatio)){
      train_ratio = as.numeric(configurationJSON$evaluation.trainRatio)
      }
      set.seed(seed)
      sample <- sample.int(n = nrow(df), size = floor(trainRatio*nrow(df)), replace = F)
      traindf <- df[sample, ]
      testdf  <- df[-sample, ]

      return (testdf)
    }
  )
)