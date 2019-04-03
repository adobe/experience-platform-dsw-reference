# _retail_ Sample App

Sample Scala Recipe using the retail data.

# Workflow
 
1. The recipe loads the dataset.
2. Feature engineering is done on the data so that the data can be used for machine learning training. 
3. The feature pipeline defines the stages with the Gradient Boosting Regressor as the chosen model.
4. This pipeline is used to fit the training data and the trained model is created. 
5. The model is transformed with the scoring dataset. 
6. Interesting columns of the output are then selected and saved back to the platform with the associated data.

# Prerequisites

To run the recipe in any org, we would need the schema of the dataset(if not uploaded previously),the input dataset, output schema and empty output dataset uploaded to the platform UI.
If all of these are previously uploaded in your org you can directly go to the section `Steps to run training and scoring jobs`
Make sure that the name of the schema and the dataset ids match the ones being supplied in `Sample config json`

### Upload Schema
Uploading a schema involves the following steps:
1. Get tenant Id
2. Create a class
3. Create a mixin
4. Create a schema

#### Get Tenant ID
        curl -X GET \
          https://platform.adobe.io/data/foundation/schemaregistry/stats \
          -H 'Authorization: Bearer {{token}} \ - Get the token from cookies of the UI
          -H 'x-api-key: acp_machineLearning_customer' \
          -H 'x-gw-ims-org-id: {{org_id}}' - Replace with your orgId 
          
          RESPONSE:
          
          {
              "imsOrg": "20656D0F5B9975B20A495E23@AdobeOrg",
              "tenantId": "acpmlexploratoryexternal"
          }

#### Create Class
        curl -X POST \
          https://platform.adobe.io/data/foundation/schemaregistry/tenant/classes \
          -H 'Authorization: Bearer {{token}} \- Get the token from cookies of the UI
          -H 'content-type: application/json' \
          -H 'x-api-key: acp_machineLearning_customer' \
          -H 'x-gw-ims-org-id: {{org_id}}' \ - Replace with your orgId
          -d '{
          "type": "object",
          "title": "ClassForRetailData",
          "auditable": true,
          "meta:extends": [
            "https://ns.adobe.com/xdm/data/time-series"
          ],
          "description": "Class for Retail Data",
          "allOf": [
            {
              "$ref": "https://ns.adobe.com/xdm/data/time-series"
            }
          ]
        }
        
        RESPONSE:
        
        {
            "$id": "https://ns.adobe.com/acpmlexploratoryexternal/classes/bef436683dae77dc57271d4c03204ac1",
            "meta:altId": ""_acpmlexploratoryexternal.classes.bef436683dae77dc57271d4c03204ac1",
            "version": "1.0"
        }


#### Create Mixin
        curl -X POST \
          https://platform.adobe.io/data/foundation/schemaregistry/tenant/mixins \
          -H 'Authorization: Bearer {{token}}\ - Get the token from cookies of the UI
          -H 'content-type: application/json' \
          -H 'x-api-key: acp_machineLearning_customer' \
          -H 'x-gw-ims-org-id: {{org_id}}' \ - Replace with your orgId
          -d '{
          "type": "object",
          "title": "MixinForRetailData",
          "description": "MixinForRetailData",
          "meta:intendedToExtend": [
            "{{$id}}" - This id is from the above response of the create class
          ],
          "definitions": {
            "retail": {
              "properties": {
                "{{tenantId}}": { - Replace this with the tenantId from from Get Tenant ID 
                call
                    "type":"object",
                    "properties": {
                       "date": {
                          "title": "date",
                          "type": "string",
                          "description": "date"
                    	},
                    	"store": {
                          "title": "store",
                          "type": "integer",
                          "description": "store"
                    	},
                    	"storeType": {
                          "title": "storeType",
                          "type": "string",
                          "description": "storeType"
                    	},
                    	"weeklySales": {
                          "title": "weeklySales",
                          "type": "number",
                          "description": "weeklySales"
                    	},
                    	"storeSize": {
                          "title": "storeSize",
                          "type": "integer",
                          "description": "storeSize"
                    	},
                    	"temperature": {
                          "title": "temperature",
                          "type": "number",
                          "description": "temperature"
                    	},
                    	"regionalFuelPrice": {
                          "title": "regionalFuelPrice",
                          "type": "number",
                          "description": "regionalFuelPrice"
                    	},
                    	"markdown": {
                          "title": "markdown",
                          "type": "number",
                          "description": "markdown"
                    	},
                    	"cpi": {
                          "title": "cpi",
                          "type": "number",
                          "description": "cpi"
                    	},
                    	"unemployment": {
                          "title": "unemployment",
                          "type": "number",
                          "description": "unemployment"
                    	},
                    	"isHoliday": {
                          "title": "isHoliday",
                          "type": "boolean",
                          "description": "isHoliday"
                    	}
                	}
                }
              }
            }
          },
          "allOf": [
            {
              "$ref": "#/definitions/retail"
            }
          ]
        }
        
        RESPONSE:
            {
                "meta:altId": "_acpmlexploratoryexternal.mixins.0e63845403bffa4930ad2517fcc50f77",
                "meta:xdmType": "object",
                "$id": "https://ns.adobe.com/acpmlexploratoryexternal/mixins/0e63845403bffa4930ad2517fcc50f77"
            }
#### Create Schema
        curl -X POST \
          https://platform.adobe.io/data/foundation/schemaregistry/tenant/schemas \
          -H 'Authorization: Bearer {{token}} \
          -H 'content-type: application/json' \
          -H 'x-api-key: acp_machineLearning_customer' \
          -H 'x-gw-ims-org-id: {{org_id}}' \ - Replace with your orgId
          -d '{
          "type": "object",
          "title": "SchemaForRetailData",
          "auditable": true,
          "meta:extends": [
            "{{$id}}", - Get this value from Create Class, in ths eg. the value is  "https://ns.adobe
            .com/acpmlexploratoryexternal/classes/bef436683dae77dc57271d4c03204ac1"
            "{{$id}}" - Get this value from Create Mixin - in ths eg. the value is "https://ns.adobe
            .com/acpmlexploratoryexternal/mixins/0e63845403bffa4930ad2517fcc50f77"
          ],
          "description": "Retail Schema",
          "allOf": [
            {
                    "$ref": "{{$id}}", - Get this value from Create Class, in ths eg. the value is  "https://ns.adobe
                                        .com/acpmlexploratoryexternal/classes/bef436683dae77dc57271d4c03204ac1"
                },
                {
                    "$ref": "{{$id}}" - Get this value from Create Mixin - in ths eg. the value is "https://ns.adobe
                                        .com/acpmlexploratoryexternal/mixins/0e63845403bffa4930ad2517fcc50f77"
                }
          ]
        }
        
        RESPONSE:
        {
            "meta:altId": "_acpmlexploratoryexternal.schemas.4fb4c8779c692fb7643c19e6009a8542",
            "meta:xdmType": "object",
            "$id": "https://ns.adobe.com/acpmlexploratoryexternal/schemas/4fb4c8779c692fb7643c19e6009a8542"
        }
        
### Upload Dataset from UI             

Upload the json from here:
`https://github.com/adobe/experience-platform-dsw-reference/blob/master/datasets/retail/XDM0.9.9
.9/DSWRetailSalesForXDM0.9.9.9.json`


Create a dataset with "SchemaForRetailData" schema and the json file as the source.
Please look at the `Video to create dataset and upload file` to platform UI.

### Video to create dataset and upload file

[![Watch the video](../../docs/images/HomePage.png)](https://youtu.be/v1QIlCe5dgw)

### Upload output schema 

Upload the output schema (schema should have "prediction:Number, store:Integer, date:String"). 
Please refer to the curl commands above to Create Class, Create Mixin, Create Schema for output data with naming them
 appropriately. In this example,
the output class is named "ClassForRetailOutput", output mixin is named "MixinForRetailOuputData" and output schema is "SchemaForRetailOutputData"
The mixin should have the following properties:

        "properties": {
               "date": {
                  "title": "date",
                  "type": "string",
                  "description": "date"
            	},
            	"store": {
                  "title": "store",
                  "type": "integer",
                  "description": "store"
            	},
            	"prediction": {
                  "title": "prediction",
                  "type": "number",
                  "description": "prediction"
            	}
            	
        }
        
Create an empty dataset with this schema. 
Please look at the video `Video to create dataset and upload file`. 
(Do not have to upload any json for this because we want an empty dataset)
Get this datasetId and plug it in pipelineservice.json. For eg: it is referenced as scoredDatasetId in the sample json. All the prerequisites are complete and you can now proceed to running some training and scoring jobs. 


# Steps to run training and scoring jobs

git clone this repository from `https://github.com/adobe/experience-platform-dsw-reference`


cd to recipes/scala and run `build.sh` 

```
sh ./build.sh
```

This generates a fat jar and is saved in the target directory of the project. 
Use this jar and go to platform UI and run training and scoring. 
Please look at the video `Video for Training, Scoring and Saving data`

### Video for Training, Scoring and Saving data
[![Watch the video](../../docs/images/HomePage.png)](https://youtu.be/SmOD-LBISwU)


# Sample Config json
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
                        "value": "date,store,storeType,storeSize,temperature,regionalFuelPrice,markdown,cpi,unemployment,isHoliday"
                    },
                    {
                        "key": "apiKey",
                        "value": "acp_machineLearning_customer"
                    },
                    {
                        "key": "ACP_DSW_TARGET_FEATURES",
                        "value": "weeklySales"
                    },
                    {
                        "key": "ACP_DSW_FEATURE_UPDATE_SUPPORT",
                        "value": false
                    },
                    {
                        "key": "ACP_DSW_TRAINING_XDM_SCHEMA",
                        "value": "https://ns.adobe.com/acpmlexploratoryexternal/schemas/4fb4c8779c692fb7643c19e6009a8542"
                    },
                    {
                        "key":"tenantId",
                        "value": "_acpmlexploratoryexternal"
                    },
                    {
                        "key":"batchId",
                        "value": "cef66f5531e44037a44071300ad95337"
                    },
                    {
                       "key": "timeframe",
                       "value": "600000000"
                    }
                ]
            },
            {
                "name": "score",
                "parameters": [
                    {
                        "key": "apiKey",
                        "value": "acp_machineLearning_customer"
                    },
                    {
                        "key": "scoredDataSetId",
                        "value": "5ca3c1f12a7d4114b357da4d"
                    },
                    {
                        "key": "timeframe",
                        "value": "600000000"
                    },
                    {
                        "key":"ACP_DSW_SCORING_RESULTS_XDM_SCHEMA",
                        "value":"https://ns.adobe.com/acpmlexploratoryexternal/schemas/f54e82c6625daba3c12b3e7a2590fa5c"
                    },
                    {
                        "key":"batchId",
                        "value": "cef66f5531e44037a44071300ad95337"
                    },
                    {
                        "key":"tenantId",
                        "value": "_acpmlexploratoryexternal"
                    }
        
                ]
            }
        ]
