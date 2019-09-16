#####################################################################
# ADOBE CONFIDENTIAL
# ___________________
#
#  Copyright 2017 Adobe
#  All Rights Reserved.
#
# NOTICE:  All information contained herein is, and remains
# the property of Adobe and its suppliers, if any. The intellectual
# and technical concepts contained herein are proprietary to Adobe
# and its suppliers and are protected by all applicable intellectual
# property laws, including trade secret and copyright laws.
# Dissemination of this information or reproduction of this material
# is strictly forbidden unless prior written permission is obtained
# from Adobe.
#####################################################################

import os as os
os.environ["ENV_CATALOG_URL"] = "https://platform.adobe.io/data/foundation/catalog/"
os.environ["ENV_QUERY_SERVICE_URL"] = "https://platform.adobe.io/data/foundation/query"
os.environ["ENV_BULK_INGEST_URL"] = "https://platform.adobe.io/data/foundation/import/"
os.environ["ENV_REGISTRY_URL"] = "https://platform.adobe.io/data/foundation/schemaregistry/tenant/schemas"

from .trainingdataloader import load
from .pipeline import train
from .scoringdataloader import load
from .datasaver import save
