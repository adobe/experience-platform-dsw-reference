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

from nltk.classify import NaiveBayesClassifier
import collections
import nltk.metrics
import nltk.classify.util
import nltk

def train(configProperties, data):

    classifier = NaiveBayesClassifier.train(data)
    #print('accuracy:', nltk.classify.util.accuracy(classifier, testfeats))
    classifier.show_most_informative_features()
    return classifier


def score(configProperties, data, model):

    refsets = collections.defaultdict(set)
    testsets = collections.defaultdict(set)

    for i, (feats, label) in enumerate(data):
        refsets[label].add(i)
        observed = model.classify(feats)
        testsets[observed].add(i)

    return testsets
