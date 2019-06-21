# _retail_ Sample App

Sample Python recipe using the retail data.

# Workflow
 
1. The recipe loads the dataset
2. Feature engineering is done on the data so that the data can be used for machine learning training
3. The feature pipeline defines the stages with the Gradient Boosting Regressor as the chosen model
4. This pipeline is used to fit the training data and the trained model is created 
5. The model is transformed with the scoring dataset
6. Interesting columns of the output are then selected and saved back to the platform with the associated data

# Prerequisites

To run the recipe in any org, we would need the schema of the dataset, the input dataset, 
output schema and empty output dataset uploaded to the platform UI. For setting this up, use the bootstrap script 
within `/acp-data-services-dsw-reference/bootstrap`
Get the tenant id from the bootstrap script and replace the value in the `retail.config.json` 
If you got the engine artifact from the bootstrap script, jump to the section `Video for Training, Scoring and 
Saving data` 

# Steps:

git clone this repository from `https://github.com/adobe/experience-platform-dsw-reference`

cd python/retail/ and run

```
sh ./login.sh
sh ./build.sh
```

Please note the `login.sh` script should only need to be run once.

### Video for Training, Scoring and Saving data
[![Watch the video](../../docs/images/HomePage.png)](https://youtu.be/rur0jkqhvno)

# Sample Configuration File
Sample configuration json to be used with the recipe.
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
            "key": "tenantId",
            "value": "_<tenant_id>
         },
         {
           "key": "ACP_DSW_TRAINING_XDM_SCHEMA",
           "value": ""
         },
         {
           "key": "evaluation.labelColumn",
           "value": "weeklySalesAhead"
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
                    "key": "tenantId",
                    "value": "_<tenant_id>"
                },
                {
                  "key":"ACP_DSW_SCORING_RESULTS_XDM_SCHEMA",
                  "value":""
                }
            ]
      }
    ]
```


