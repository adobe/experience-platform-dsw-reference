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

from pyspark.ml import Pipeline
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.feature import HashingTF, Tokenizer
from pyspark.sql import SparkSession

def apply(configProperties):

    # Reading configs from config properties.
    maxIterVal = int(configProperties.get("maxIter"))
    regParamVal = float(configProperties.get("regParam"))
    #numFeaturesVal: Int  = configProperties.get("numFeatures").get.toInt

    # Configure an ML pipeline, which consists of three stages: tokenizer, hashingTF, and lr.
    tokenizer = Tokenizer(inputCol="text", outputCol="words")
    hashingTF = HashingTF(inputCol=tokenizer.getOutputCol(), outputCol="features")
    lr = LogisticRegression(maxIter=maxIterVal, regParam=regParamVal)
    pipeline = Pipeline(stages=[tokenizer, hashingTF, lr])

    return pipeline

def getParamMap(configProperties, sparkSession):
    return None
