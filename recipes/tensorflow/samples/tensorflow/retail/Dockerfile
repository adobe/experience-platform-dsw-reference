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

FROM adobe/acp-dsw-ml-runtime-python-gpu:2.0.2

# Copy the necessary recipe files to build
COPY setup.py /root/retail/
COPY retail /root/retail/retail/

# Build, install and clean up the recipe
WORKDIR /root/retail
RUN python setup.py install
RUN cp dist/samples_tensorflow*.egg /application.egg && \
    rm -rf /root/retail

ENV PYTHONPATH=$PYTHONPATH:/application.egg

# Show the python environment
RUN conda list
