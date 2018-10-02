# _Template_ App

The Template Recipe serves as a shell for building _Data Science Workspace Recipes_

# Steps:

git clone this repository

Navigate the directory to the one containing `build.sh` file

sh ./build.sh

# Recipe Development Files

:page_facing_up: `./login.sh`

Docker Login utility. This file will ask for your Docker Registry credentials provided by the Data Science Workspace, within the _Recipe Import_ Workflow. Run it as such:

```
sh ./login.sh
```

You will be asked for Docker Host, Username, and Password.

:page_facing_up: `./build.sh`

Docker Image Building utility. Running this file will enable you to build an push your recipe as a Docker image to the provided Docker Registry. To run it:

```
sh ./build.sh
```

You will be prompted for Recipe Image version and Docker Host. Once the image is pushed you will be presented with the URL to your hosted Recipe Docker Image.


:page_facing_up: `./Dockerfile`

This file lists all the dependencies your recipe requires to run properly. It is important to add into the `Dockerfile` all packages and libraries that need to be installed on the system that will run your recipe.


:page_facing_up: `./setup.py`

This file defines the entry points of the classes and methods required by the Machine Learning Framework to execute tasks related to data loading, training, scoring, and data saving.

:page_facing_up: `./template/datasaver.py`

Following a scoring task `datasaver.save(configProperties, prediction)` is called to ensure the developer is given a way to persist evaluated predictions.

:page_facing_up: `./template/pipeline.py`

The pipeline is the class that is tasked with defining the methods required for training and scoring.

`pipeline.train(configProperties, data)` takes the config properties and the data loaded via `scoringdataloader.py`. You will write your training model (or its entry point) within that method.

`score(configProperties, data, model)` is passed the model instance so that predictions can be called, using methods such as `model.predict()` depending on your model implementation.


:page_facing_up: `./template/scoringdataloader.py`

This class defines the `scoringdataloader.load(configProperties)` method. Its goal is to load the scoring data and return it to the framework, usually in the form of a dataframe.

:page_facing_up: `./template/trainingdataloader.py`

This class defines the `trainingdataloader.load(configProperties)` method. Its goal is to load the training data and return it to the framework, usually in the form of a dataframe.


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

