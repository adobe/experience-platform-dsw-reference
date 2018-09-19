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
abstractEvaluator <- ml.runtime.r::abstractEvaluator

#' applicationEvaluator
#'
#' @keywords applicationEvaluator
#' @export applicationEvaluator
#' @exportClass applicationEvaluator
applicationEvaluator <- setRefClass("applicationEvaluator",
                                    contains = "abstractEvaluator",
                                    methods = list(
                                      evaluate = function(configurationJSON) {
                                        print("Running Evaluation Function.")
                                        values <- {}
                                        values$name <- "metric1"
                                        values$value <- "value1"
                                        values$valueType <- "type1"
                                        values2 <- {}
                                        values2$name <- "metric2"
                                        values2$value <- "value2"
                                        values2$valueType <- "type2"
                                        metrics <- list(values, values2)
                                        return(metrics)
                                      }
                                    )
)