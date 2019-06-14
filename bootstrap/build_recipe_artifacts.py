'''
 * ADOBE CONFIDENTIAL
 * ___________________
 *
 *  Copyright 2019 Adobe Systems Incorporated
 *  All Rights Reserved.
 *
 * NOTICE:  All information contained herein is, and remains
 * the property of Adobe Systems Incorporated and its suppliers,
 * if any.  The intellectual and technical concepts contained
 * herein are proprietary to Adobe Systems Incorporated and its
 * suppliers and are protected by all applicable intellectual property
 * laws, including trade secret and copyright laws.
 * Dissemination of this information or reproduction of this material
 * is strictly forbidden unless prior written permission is obtained
 * from Adobe Systems Incorporated.
'''

import subprocess
import os
from utils import setup_logger

LOGGER = setup_logger(__name__)

def build_recipe_artifacts(kernel_type):
    """

    :param kernel_type: kernel type - Value must be one of Spark, Pyspark, Python, R
    :return: None
    """
    if kernel_type.lower() == "pyspark":
        os.chdir("../recipes/pyspark")
        subprocess.call(['./build.sh'])
    elif kernel_type.lower() == "spark":
        os.chdir("../recipes/scala")
        subprocess.call(['./build.sh'])
    elif kernel_type.lower() == "python":
        os.chdir("../recipes/python/retail")
        if subprocess.call(['./login.sh']) == 0:
            subprocess.call(['./build.sh'])
    elif kernel_type.lower() == "r":
        os.chdir("../recipes/R/Retail - GradientBoosting")
        if subprocess.call(['./login.sh']) == 0:
            subprocess.call(['./build.sh'])
    else:
        LOGGER.error("Invalid kernel type")