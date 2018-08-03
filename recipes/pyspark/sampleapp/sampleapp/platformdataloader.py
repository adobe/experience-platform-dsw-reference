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

from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField
from pyspark.sql.types import LongType, DoubleType, IntegerType, StringType

CLIENT_ID = "imsClientId"
CLIENT_SECRET = "CONF_imsClientSecret_VALUE"
CLIENT_CODE = "CONF_imsClientCode_VALUE"
API_KEY = "apiKey"
DATASET_ID = "dataSetId"
BATCH_ID = "batchId"
ORG_ID = "orgId"
PLATFORM_DATASET_PACKAGE = "com.adobe.platform.dataset"

def load(configProperties, spark):

  clientSecret = str(spark.sparkContext.getConf.get(CLIENT_SECRET,""))
  clientCode = str(spark.sparkContext.getConf.get(CLIENT_CODE,""))
  clientId = str(configProperties.get(CLIENT_ID))
  apiKey = clientId
  dataSetId = str(configProperties.get(DATASET_ID))
  orgId = str(configProperties.get(ORG_ID))
  batchId = str(configProperties.get(BATCH_ID))

  for arg in ['clientSecret', 'clientCode', 'clientId', 'apiKey', 'dataSetId', 'orgId']:
    if eval(arg) == 'None':
      raise ValueError("%s is empty" % arg)

  reader = spark.read.format(PLATFORM_DATASET_PACKAGE)\
    .option('clientId', clientId)\
    .option('clientCode', clientCode)\
    .option('clientSecret', clientSecret)\
    .option('apiKey', apiKey)\
    .option('orgId', orgId)

  if batchId != 'None':
    reader = reader.option('batchId', batchId)

  training = reader.load(dataSetId)

  return training
