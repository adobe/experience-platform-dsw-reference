alsdemo_data contains train/test datasets for Alternating Least Square (ALS) modeling. 
Both datasets contains 3 columns: userid, catid, ratings. 

The datasets are created from a real e-commerce analytics data as follows
* extract columns containing visitor-id, product categories information, and visitors' activities
* convert original visitor-id to index (start from 0) and renamed as “userid”
* create a product-taxonomy from extracted product categories, choose product categories at appropriate level which are converted to “catid”
* compute visotors' rating of the products using extracted visitors online activities such as search, view, add-to-cart, checkout, purchase
* split the feature dataset to train dataset (the first 7 days) and test dataset (the last one day)
* sample 1% train/test datasets (at the visitor-level)

