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

from setuptools import setup,find_packages

setup(name='retail',
      version='0.0.1',
      packages=['retail'],
      package_data={'retail': ['resources/*']},
      entry_points={
        'Training': [
            'training_dataloader=retail.trainingdataloader',
            'training_pipeline=retail.pipeline'
        ],
        'Scoring': [
            'scoring_dataloader=retail.scoringdataloader',
            'scoring_pipeline=retail.pipeline',
            'scoring_datasaver=retail.datasaver'
        ],
        'Evaluation': [
            'evaluator=retail.evaluator:Evaluator'
        ]
        }
      )
