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
from ml.runtime.python.Interfaces.AbstractEvaluator import AbstractEvaluator

import os
import pickle

class Evaluator(AbstractEvaluator):
    def __init__(self):
        print('Initiate')

    def evaluate(self, data=[], model={}, config={}):
        print('Evaluation evaluate triggered')
        metrics_dict = pickle.load(open(os.path.join(config['modelPATH'], 'metrics_dict.pkl'), 'rb'))

        metrics = []
        for key in metrics_dict.keys():
            metrics.append({'name': key, 'value': float(metrics_dict[key]), 'valueType': 'double'})

        return metrics

    def split(self, config={}):

        print('Split triggered')
        return 'train', 'test'
