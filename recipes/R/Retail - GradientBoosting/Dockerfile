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

FROM adobe/acp-dsw-ml-runtime-r:0.24.8

RUN install2.r gbm
RUN install2.r lubridate
RUN install2.r tidyverse
RUN install2.r evaluators.r.tar.gz


WORKDIR /root/sample/code

COPY . .

RUN R -e 'library(devtools);document()'
RUN R --no-site-file --no-environ --no-save --no-restore --quiet CMD build . --no-resave-data

RUN cp *.tar.gz /root/runtime/ml.retail.r.tar.gz

RUN rm -rf /root/sample/code


WORKDIR /root/runtime

RUN install2.r -l /root/sample  ml.retail.r.tar.gz
