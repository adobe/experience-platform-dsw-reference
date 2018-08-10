#
# Copyright 2017 Adobe.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

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

      # Load data
      cars_data <- read.csv(configurationJSON$data)

      # Create training and test set
      split_size <- floor(0.8 * nrow(cars_data))
      set.seed(1234)
      train_index <- sample(seq_len(nrow(cars_data)), size = split_size)
      train <- cars_data[train_index, ]
      test <- cars_data[-train_index, ]

      # Retrieve saved model from trainer
      retrieved_model <- readRDS("model.rds")

      # Evaluate Performance
      predictions <- predict(retrieved_model, test)
      rmse <- sqrt(mean((predictions - test$dist)^2))
      print(paste("Test Set RMSE: ", rmse, sep = ""))

      print("Exiting Scorer Function.")
    }
  )
)
