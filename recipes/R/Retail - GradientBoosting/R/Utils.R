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

Utils <- setRefClass(
  Class = "Utils",
  methods = list(
    mapFields = function(df) {

      # Rename columns
      df <- setNames(df, c("id","eventType","timestamp", "cpi","date", "isHoliday","markdown",
                           "regionalFuelPrice", "store","storeSize","storeType","temperature",
                           "unemployment","weeklySales"))

      #Drop id,eventType and timestamp
      df <- subset(df, select= -c(id,eventType,timestamp))

      return (df)
    }
  )
)