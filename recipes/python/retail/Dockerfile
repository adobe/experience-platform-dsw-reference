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

FROM adobe/acp-dsw-ml-runtime-python:0.27.0

#INSTALL modules needed by application
RUN /usr/bin/python3.5 -m pip install -U numpy==1.16.2
RUN /usr/bin/python3.5 -m pip install -U pandas==0.24.2
RUN /usr/bin/python3.5 -m pip install -U scikit-learn==0.20.3
RUN /usr/bin/python3.5 -m pip install -U scipy==1.2.1
RUN /usr/bin/python3.5 -m pip install -U fastparquet==0.2.1

WORKDIR /root/retail

COPY . .

RUN python setup.py clean --all install

COPY dist/retail*.egg /application.egg

ENV PYTHONPATH=$PYTHONPATH:/application.egg
