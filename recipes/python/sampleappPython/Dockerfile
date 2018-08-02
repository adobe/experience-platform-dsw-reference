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

FROM [[Docker Artifactory URL]]/ml-runtime-python:0.0.2

#INSTALL NLTK and other modules needed by application
RUN /usr/bin/python3.5 -m pip install -U nltk
RUN /usr/bin/python3.5 -m pip install -U numpy

COPY dist/sampleapp*.egg /application.egg

ENV PYTHONPATH=$PYTHONPATH:/application.egg

