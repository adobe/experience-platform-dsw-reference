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

from setuptools import setup, find_packages

setup(
    name='samples-tensorflow',
    version='0.0.1',
    url='',
    license='',
    author='',
    author_email='',
    packages=find_packages(),
    description='',
    entry_points={
        'Training': [
            'trainer=retail.tensorflow.trainer:Trainer'
        ],
        'Scoring': [
            'scorer=retail.tensorflow.scorer:Scorer'
        ],
        'Evaluation': [
            'evaluator=retail.tensorflow.evaluator:Evaluator'
        ]
    }
)
