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

FROM adobe/acp-dsw-ml-runtime-python:0.9.0

#INSTALL NLTK and other modules needed by application
RUN /usr/bin/python3.5 -m pip install -U numpy
RUN /usr/bin/python3.5 -m pip install -U pandas
RUN /usr/bin/python3.5 -m pip install -U sklearn
RUN /usr/bin/python3.5 -m pip install -U scipy

COPY dist/retail*.egg /application.egg

ENV PYTHONPATH=$PYTHONPATH:/application.egg

