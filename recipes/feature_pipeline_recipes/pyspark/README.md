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


cd to recipes/feature_pipeline_recipes/pyspark and run `build.sh`

```
sh ./build.sh
```
Enter your admin password when prompted for
This generates an egg and is saved in the dist directory of the project
Use this egg and exercise the calls in the postman collection below:
https://www.getpostman.com/collections/86934cae537aae60d052


For the details on executing the postman calls:
1. Create an engine with a call to POST Feature Pipeline Engine EGG:
    i) Supply the pipeline.json as form-data to the engine key

   ii) The egg file generated above is the value for the keys 'featurePipelineOverrideArtifact' and 'defaultArtifact'

2. Post Instance
3. Post Experiment
4. Post Feature Pipeline Experiment Run
5. Get experiment status and wait to be DONE
6. Post Training Experiment Run
7. Get experiment status and wait to DONE
8. Post Scoring Experiment Run
9. Get experiment status and wait to DONE
