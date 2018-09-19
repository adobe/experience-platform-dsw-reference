# _retail_ Sample App

Sample R recipe using the retail data.

# Steps:

git clone this repository

Navigate the directory to the one containing `build.sh` file

./build.sh


# Sample Configuration File
Sample configuration json to be used with the recipe.
```
[
  {
    "name": "train",
    "parameters": [
      {
        "key": "ACP_DSW_INPUT_FEATURES",
        "value": "date, store, storeType. storeSize, temperature, regionalFuelPrice, markdown, cpi, unemployment, isHoliday"
      },
      {
        "key": "ACP_DSW_TARGET_FEATURES",
        "value": "weeklySales"
      },
      {
        "key": "ACP_DSW_FEATURE_UPDATE_SUPPORT",
        "value": "false"
      },
      {
        "key": "ACP_DSW_TRAINING_XDM_SCHEMA",
        "value": "_customer/default/DSWRetailSales"
      },
      {
        "key": "trainingDataSetId",
        "value": ""
      }
  	]
  },
  {
    "name": "score",
    "parameters": [
      {
        "key": "ACP_DSW_INPUT_FEATURES",
        "value": "date, store, storeType. storeSize, temperature, regionalFuelPrice, markdown, cpi, unemployment, isHoliday"
      },
      {
        "key": "ACP_DSW_TARGET_FEATURES",
        "value": "weeklySales"
      },
      {
        "key": "ACP_DSW_FEATURE_UPDATE_SUPPORT",
        "value": "false"
      },
      {
        "key": "ACP_DSW_TRAINING_XDM_SCHEMA",
        "value": "_customer/default/DSWRetailSales"
      },
      {
        "key": "scoringDataSetId",
        "value": ""
      }

    ]
  }
]
```
