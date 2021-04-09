#
# Copyright 2017 Adobe.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

FROM adobe/acp-dsw-ml-runtime-python-gpu:1.1.1

# Install modules needed by application that aren't already part
# of the base image
RUN conda install --yes -c pytorch \
        pytorch=1.6.0 \
        torchvision=0.7.0

WORKDIR /root/samples
COPY . .

RUN python setup.py install
