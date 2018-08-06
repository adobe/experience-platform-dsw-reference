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

#Build sample python app
sudo python setup.py install

docker build --pull -t [DOCKER ARTIFCATORY URL]/ml-retaildemo-python:0.0.1 .
docker push [DOCKER ARTIFCATORY URL]/ml-retaildemo-python:0.0.1

echo "[DOCKER ARTIFCATORY URL]/ml-retaildemo-python:0.0.1"
