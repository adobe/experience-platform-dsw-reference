# _retail_ Sample App

Sample PySpark Recipe using the retail data.

# Workflow
 
1. The recipe loads the dataset
2. Feature engineering is done on the data so that the data can be used for machine learning training
3. The feature pipeline defines the stages with the Gradient Boosting Regressor as the chosen model
4. This pipeline is used to fit the training data and the trained model is created
5. The model is transformed with the scoring dataset
6. Interesting columns of the output are then selected and saved back to the platform with the associated data

# Prerequisites

To run the recipe in any org, we would need the schema of the dataset,the input dataset, 
output schema and empty output dataset uploaded to the platform UI. For setting this up, use the bootstrap script 
within `/acp-data-services-dsw-reference/bootstrap`
Get the tenant id from the bootstrap script and replace the value in the `pipeline.json` 
If you got the engine artifact from the bootstrap script, jump to the section `Video for Training, Scoring and 
Saving data` 

# Steps to run training and scoring jobs

git clone this repository from `https://github.com/adobe/experience-platform-dsw-reference`


cd to recipes/pyspark and run `build.sh` 

```
sh ./build.sh
```
Enter your admin password when prompted for.
This generates an egg and is saved in the dist directory of the project. 
Use this egg and go to platform UI `https://platform.adobe.io` and run training and scoring. 
Please look at the video `Video for Training, Scoring and Saving data`

### Video for Training, Scoring and Saving data
[![Watch the video](../../docs/images/HomePage.png)](https://youtu.be/Ob_o0FgRXU4)

# Sample Config json
```
    [
      {
        "name": "train",
        "parameters": [
          {
            "key": "learning_rate",
            "value": "0.1"
          },
          {
            "key": "n_estimators",
            "value": "100"
          },
          {
            "key": "max_depth",
            "value": "3"
          },
          {
            "key": "ACP_DSW_INPUT_FEATURES",
            "value": ""
          },
          {
            "key": "ACP_DSW_TARGET_FEATURES",
            "value": ""
          },
          {
            "key": "ACP_DSW_FEATURE_UPDATE_SUPPORT",
            "value": false
          },
          {
            "key":"tenant_id",
            "value": "_<tenant_id>"
          },
          {
            "key": "ACP_DSW_TRAINING_XDM_SCHEMA",
            "value": ""
          },
          {
            "key": "timeframe",
            "value": "600000000"
          },
          {
            "key": "evaluation.labelColumn",
            "value": "weeklySalesAhead"
          },
          {
            "key": "evaluation.scalingColumn",
            "value": "weeklySalesScaled"
          },
          {
            "key": "evaluation.predictionColumn",
            "value": "prediction"
          },
          {
            "key": "evaluation.trainRatio",
            "value": "0.8"
          },
          {
            "key": "evaluation.metrics",
            "value": "MAPE,MAE,RMSE,MASE"
          }
        ]
      },
      {
        "name": "score",
        "parameters": [
          {
            "key":"tenant_id",
            "value": "_<tenant_id>"
          },
          {
            "key": "timeframe",
            "value": "600000000"
          },
          {
            "key": "evaluation.predictionColumn",
            "value": "prediction"
          },
          {
            "key":"ACP_DSW_SCORING_RESULTS_XDM_SCHEMA",
            "value":""
          }
        ]
      }
    ]
```
Note : 
Filtering rows in dataset is possible with timeframe property. 
This property must be specified in minutes.
Filtering is calculated : current time - timeframe.
