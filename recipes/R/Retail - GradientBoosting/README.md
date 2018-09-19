# _retail_ Sample App

Sample R recipe using the retail data.

# Steps:

git clone this repository

Navigate the directory to the one containing `build.sh` file and run

```
sh ./login.sh
sh ./build.sh
```

Please note the `login.sh` script should only need to be run once.


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
