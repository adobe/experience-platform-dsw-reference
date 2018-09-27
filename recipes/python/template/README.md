# _Template_ App

The Template Recipe serves as a shell for building _Data Science Workspace Recipes_

# Steps:

git clone this repository

Navigate the directory to the one containing `build.sh` file

sh ./build.sh

# Recipe Development Files

`login.sh` - Docker Login utility. This file will ask for your Docker Registry credentials provided by the Data Science Workspace, within the _Recipe Import_ Workflow. Run it as such:

```
sh ./login.sh
```
You will be asked for Docker Host, Username, and Password.

`build.sh` - Docker Image Building utility. Running this file will enable you to build an push your recipe as a Docker image to the provided Docker Registry. To run it:

```
sh ./build.sh
```
You will be prompted for Recipe Image version and Docker Host. Once the image is pushed you will be presented with the URL to your hosted Recipe Docker Image.


`Dockerfile` - This file lists all the dependencies your recipe requires to run properly. It is important to add into the `Dockerfile` all packages and libraries that need to be installed on the system that will run your recipe.


`setup.py` - This file defines the entry points of the classes and methods required by the Machine Learning Framework to execute tasks related to data loading, training, scoring, and data saving.

`datasaver.py` - Following a scoring task `datasaver.save(configProperties, prediction)` is called to ensure the developer is given a way to persist evaluated predictions.

# Sample Configuration File
Sample configuration json to be used with the recipe.
```
[
  {
    "name": "train",
    "parameters": [
      {
        "key": "data",
        "value": "https://raw.githubusercontent.com/adobe/acp-data-services-dsw-reference/master/datasets/retail/retail.csv"
      },
      {
        "key": "train_start",
        "value": "2010-02-12"
      },
      {
        "key": "train_end",
        "value": "2012-04-06"
      }
    ]
  },
    {
    "name": "score",
    "parameters": [
      {
        "key": "data",
        "value": "https://raw.githubusercontent.com/adobe/acp-data-services-dsw-reference/master/datasets/retail/retail.csv"
      },
      {
        "key": "test_start",
        "value": "2012-04-13"
      }
    ]
  }
]
```

