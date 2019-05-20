# Bootstrap script
This script is used to set up an org with the input, output schema and input, output datasets 
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

# Setup
We would need an access token to access the APIS. This can be obtained from either an Adobe IO integration or from the 
application cookies. 
### Adobe IO Integration workflow
Refer to the following documentation to create an Adobe IO integration:
`https://adobeio-prod.adobemsbasic.com/authentication/auth-methods.html#!AdobeDocs/adobeio-auth/master/AuthenticationOverview/ServiceAccountIntegration.md`

Input the values in the Enterprise of the config.yaml from the Adobe IO integration:

    Enterprise:
       api_key: []
       org_id: []@AdobeOrg
       tech_acct: [].adobe.com
       client_secret: []
       priv_key_filename: [] 
       
### Application cookies workflow
Login to platform UI - `https://platform.adobe.com`. Open the Javascript console and get the `ims-user-token` value 
from the Application cookies.
Input this value to `ims_token: []`

### Input the values for the Titles:

    Titles:
       input_class_title: []
       input_mixin_title: []
       input_mixin_definition_title: []
       input_schema_title: []
       input_dataset_title: []
       file_replace_tenant_id: DSWRetailSalesForXDM0.9.9.9.json
       file_with_tenant_id: []
       is_ouput_schema_different: True
       output_mixin_title: []
       output_mixin_definition_title: []
       output_schema_title: []
       output_dataset_title: []

# How to run
Navigate to the `bootstrap` directory and run `python bootstrap.py`
