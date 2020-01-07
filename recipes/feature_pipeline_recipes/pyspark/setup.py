#####################################################################
# ADOBE CONFIDENTIAL
# ___________________
#
#  Copyright 2020 Adobe
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

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(name='pysparkfeaturepipelineapp',
      version='0.1.0',
      packages=['pysparkfeaturepipelineapp'],
      install_requires=required,
      package_data={'pysparkfeaturepipelineapp': ['resources/*']}
    )
