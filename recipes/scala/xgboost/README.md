# XGBoost  (Scala)

## Introduction
This project implements the model-authoring sdk for creating a sample XGBoost service which can be used with the ML Framework. Step by step instructions for using the ML framework with this job can be found here - https://[[DOCUMENTATION URL]]/pages/viewpage.action?pageId=1350607803

## Project information
- pipeline.json - Default configuration for the model specification
- application.properties - Defines the classes implementing the model authoring sdk
- XGBoostPipeline.scala - Main Pipeline configuration class that outlines the xgboost pipeline stages
- ScoringDataLoader - Loader class that loads the scoring data from the blob store (This sample contains the data in the blob store associated with the HDInsights cluster
- TrainingDataLoader - Loader class that loads the training data from the blob store (This sample contains the data in the blob store associated with the HDInsights cluster
- ScoringDataSaver - Saves the output dataframe with prediction results in the blob store location specified in the configuration

## Steps
To create the assembly jar, follow the steps below
```
git clone [[GITHUB BASE URL]]:ml/samples.git
cd scala/xgboost
sbt assembly
```
To create a local jar, the following command can be used
```
sbt clean package publish-local
```