# _retail_ Sample App with Feature Pipeline

Sample PySpark Recipe using the retail data which is transformed through a feature pipeline.

# Workflow

1. The recipe loads the dataset to a pipeline
2. Feature transformation is done on the dataset and written back to the platform
3. The transformed data is loaded for training
4. The feature pipeline defines the stages with the Gradient Boosting Regressor as the chosen model
5. This pipeline is used to fit the training data and the trained model is created
6. The model is transformed with the scoring dataset
7. Interesting columns of the output are then selected and saved back to the platform with the associated data

# Prerequisites

To run the recipe in any org, we would need the schema of the dataset, the input dataset, transformed schema and empty
dataset with transformed schema, output schema and empty output dataset uploaded to the platform UI. For setting this 
up, use the bootstrap
script within `/acp-data-services-dsw-reference/bootstrap`.

# Steps to run training and scoring jobs

git clone this repository from [https://github.com/adobe/experience-platform-dsw-reference](https://github.com/adobe/experience-platform-dsw-reference)


cd to recipes/feature_pipeline_recipes/pyspark and run `login.sh`

```
sh login.sh
```
The credentials for the login can be obtained from platform UI: https://platform.adobe.com

Login and click on  Models > Recipes > Import recipe > Next

From the Select Source, in the Runtime drop down select PySpark and make sure the Artifact type drop down has docker 
selected. 
Copy paste the appropriate values when running the login.sh script.
After login is successful, run `build.sh`

```
sh build.sh
```
This pushes the docker image to the ACR for eg: the docker image that is pushed will look like 
`$host/ml-featurepipeline-pyspark:$version`

Use this docker image location and exercise the calls in the postman collection below:
https://www.getpostman.com/collections/c5fc0d1d5805a5ddd41a


For the details on executing the postman calls:
1. Create an engine with a call to POST Feature Pipeline Engine
2. Post Instance
3. Post Experiment
4. Post Feature Pipeline Experiment Run
5. Get experiment status and wait to be DONE
6. Post Training Experiment Run
7. Get experiment status and wait to DONE
8. Post Scoring Experiment Run
9. Get experiment status and wait to DONE
