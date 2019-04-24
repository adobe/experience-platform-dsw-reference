#####################################################################
# ADOBE CONFIDENTIAL
# ___________________
#
#  Copyright 2019 Adobe
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

from setuptools import setup

setup(name='pysparkretailapp',
      version='0.1.0',
      packages=['pysparkretailapp'],
      install_requires=["pyspark>=2.3.0"],
      #we will use public Adobe github repo for sdk
    dependency_links=[
          'git+ssh://git@git.corp.adobe.com/ml/model-authoring-sdk-pyspark.git@master#egg=model_authoring_sdk'],
      package_data={'pysparkretailapp': ['resources/*']}
      )