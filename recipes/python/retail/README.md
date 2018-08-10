# _retail_ Sample App

Sample python recipe using the retail data.

# Steps:

git clone this repository

Navigate the directory to the one containing `build.sh` file

sh ./build.sh


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

