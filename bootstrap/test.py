import sys
for p in sys.path:
    print(p)



    #dataset_id = get_dataset_id(create_dataset_url, headers, "test",
# "https://ns.adobe.com/acpmlexploratoryexternal/schemas/f31a4257efb55671dd37612c8c3d2441")
batch_id = get_batch_id(create_batch_url, headers, "5ccb6128a274a814b266c663")
upload_file_hardcoded(create_batch_url, headers, "RetailDataWithTenantID.json", "5ccb6128a274a814b266c663", batch_id)
close_batch(create_batch_url, headers, batch_id)
