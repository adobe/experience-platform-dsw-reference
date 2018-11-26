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
echo "Deleting previous egg binaries from dist directory"
sudo rm dist/*

echo "Building .egg binary for project"
sudo python setup.py install

echo ""
echo ""

echo "please enter the version number for your recipe's docker image"
read version

echo "Enter Docker Host"
read host

docker build --pull -t $host/ml-retailsales-python:$version .
docker push $host/ml-retailsales-python:$version

echo "$host/ml-retailsales-python:$version"
