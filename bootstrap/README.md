# Bootstrap script
This script is used to set up an org with the input, output schema and input, output datasets and the recipe artifacts
required for the recipe workflow.

# Workflow
Following are the steps the script runs through to setup the input and output datasets in the org:
1. Get the access token to access the APIs
2. Get the tenantID of the org
3. Create Retail Sales Class
4. Create Input Retail Sales Mixin with the class url
5. Create Input Retail Sales Schema with the class url and the mixin url
6. Create Input Dataset with the schema url
7. Create Batch with the dataset id
8. Replace the tenant id in the json 
9. Upload the datafile (with the tenantID from above)
10. Close the batch
11. Create Output Retail Sales Mixin with the class url from step 3
12. Create Output Retail Sales Schema with the class url and the mixin url
13. Create Output Dataset with the schema
14. Build the engine artifacts based on the configuration

# Setup
We would need an access token to access the APIs. This can be obtained from either an Adobe IO integration or from the 
application cookies. 
### Adobe IO Integration workflow
Refer to the following documentation to create an Adobe IO integration:
(https://adobeio-prod.adobemsbasic.com/authentication/auth-methods.html#!AdobeDocs/adobeio-auth/master/AuthenticationOverview/ServiceAccountIntegration.md)

Input the values in the Enterprise section of the config.yaml from the Adobe IO integration:

    Enterprise:
       api_key: []
       org_id: []@AdobeOrg
       tech_acct: [].adobe.com
       client_secret: []
       priv_key_filename: [] 
       
### Application cookies workflow
Login to Adobe Experience Platform UI - (https://platform.adobe.com). Open the JavaScript console and get the 
`ims-user-token` value from the Application cookies.

Input this value in ims_token in the Platform section of the config.yaml

`ims_token: Bearer []`

### Input the values for Platform:
    Platform:   
        ingest_data: "True" # Value must be either "True" or "False"
        build_recipe_artifacts: "False" # Value must be either "True" or "False"
        kernel_type: <kernel_type> # Value must be one of Spark, Pyspark, Python, R, example Spark

### Input the values for the Titles:

    Titles:
       input_class_title: []
       input_mixin_title: []
       input_mixin_definition_title: []
       input_schema_title: []
       input_dataset_title: []
       file_replace_tenant_id: DSWRetailSalesForXDM0.9.9.9.json
       file_with_tenant_id: []
       is_output_schema_different: "True"
       output_mixin_title: []
       output_mixin_definition_title: []
       output_schema_title: []
       output_dataset_title: []
        
# How to run
Navigate to the `bootstrap` directory and run `python bootstrap.py`

# Output of the script
1. If ingest_data is set to "True" and build_recipe_artifacts is also set to "True", the data ingestion workflow is 
executed and the recipe artifacts are generated. The output is one of the following artifacts based on the kernel_type:
    1. Spark generates a jar file
    2. PySpark generates an egg file
    3. Python and R would prompt for login and generate a source url
These artifacts are then utilized to make a recipe.    
2. If ingest_data is set to "False" (the case when the schema and datasets already exist in the org), and 
build_recipe_artifacts is set to "True", the output is one of the artifacts as mentioned above based on the kernel_type.

 
