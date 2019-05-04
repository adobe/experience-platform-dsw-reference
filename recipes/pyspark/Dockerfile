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

#FROM docker-experienceplatform-release.dr-uw2.adobeitc.com/runtimepuspark:0.0.1
FROM runtimepyspark:0.0.1
#FROM docker-experienceplatform-release.dr-uw2.adobeitc.com/sensei-ml-runtime-pyspark:0.11.0

COPY dist/pysparkretailapp*.egg /application.egg

ENV MODEL_DIR=/data/model_dir
ENV PY_FILES=/runtimePythonUtil.egg,/application.egg


# Below is needed for local test mode
COPY pipeline.json /pipeline.json

