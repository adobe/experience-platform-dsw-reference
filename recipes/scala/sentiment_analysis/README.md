# Sentiment Analysis  (Scala)

## Introduction
This project implements the model-authoring sdk for creating a sample sentiment analysis job which can be used with the ML Framework. Step by step instructions for using the ML framework with this job can be found here - https://[[DOCUMENTATION URL]]/pages/viewpage.action?pageId=1350607803

## Project information
- pipeline.json - Default configuration for the model specification
- application.properties - Defines the classes implementing the model authoring sdk
- SentimentAnalysisPipeline.scala - Main Pipeline configuration class that outlines the sentiment analysis pipeline stages
- ScoringDataLoader - Loader class that loads the scoring data from the blob store (This sample contains the data in the blob store associated with the HDInsights cluster
- TrainingDataLoader - Loader class that loads the training data from the blob store (This sample contains the data in the blob store associated with the HDInsights cluster
- ScoringDataSaver - Saves the output dataframe with prediction results in the blob store location specified in the configuration

#Passing secrets from vault in configuration/pipeline.json
Secrets can be stored in vault and the vault path should be passed in into configurations.
You need to follow convention as CONF_{name}_KEY and the corresponding value for that property is defined by CONF_{name}_VALUE. You can replace {name} with whatever you want.
They will be set to spark conf

## Steps
To create the assembly jar, follow the steps below
```
git clone [[GITHUB BASE URL]]:ml/samples.git
cd scala/sentiment_analysis
sbt assembly
```
To create a local jar, the following command can be used
```
sbt clean package publish-local 
``` 
## Testing with docker spark

Once the docker image is built for the application, you can run the spark-submit on the docker image and get the output model parameters in the local directory. 
```
docker build -t sentiment-sample .
``` 
This can be run with the docker spark like shown below for training:
```
docker run -v $(pwd)/train-model:/train-model -e CONF_blobStoreAccount_KEY=fs.azure.account.key.mlhackathon01.blob.core.windows.net -e CONF_blobStoreAccount_VALUE=*** -e modelOutput=/train-model sentiment-sample  bin/spark-submit  sh -c "bin/spark-submit --class com.adobe.platform.ml.core.Training   --conf spark.driver.extraClassPath=/application.jar --conf spark.executor.extraClassPath=/application.jar  \$APPRESOURCE test pipeline.json"
```
   
For scoring
```
docker run -v $(pwd)/train-model:/train-model -e CONF_blobStoreAccount_KEY=fs.azure.account.key.mlhackathon01.blob.core.windows.net -e CONF_blobStoreAccount_VALUE=*** sentiment-sample  bin/spark-submit  sh -c "bin/spark-submit --class com.adobe.platform.ml.core.Scoring   --conf spark.driver.extraClassPath=/application.jar --conf spark.executor.extraClassPath=/application.jar  \$APPRESOURCE test pipeline.json"
```

