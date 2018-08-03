# pyspark-samples

SampleApp is an intelligent service sample using pyspark which can be onboarded on ML Framework.

# Init file

In order to use that in the application following is required:
Define following properties on your config file:
* CONF_imsClientSecret_KEY: "imsClientSecret"
* CONF_imsClientSecret_VALUE: <Vault path to your ims client secret>
* CONF_imsClientCode_KEY: "imsClientCode"
* CONF_imsClientCode_VALUE: <Vault path to your ims client code>
* imsClientId: <Your IMS client Id>
* apiKey : <Using service tokens approach it's same as your IMSClientId>
* dataSetId: <Your dataset id>
* orgId: <Your org id>
* batchId: (Optional if you want data from specific batch)

# Steps:

`git clone [[GITHUB BASE URL]]:ml/samples-pyspark.git`

Download platform-sdk-1.0.1-with-dependencies.jar from artifactory and move it to sampleapp/dist/platform-sdk-1.0.1-with-dependencies.jar

`cd sampleapp/`

`python setup.py install`


Use the .egg file generated in dist folder to create a model spec.
