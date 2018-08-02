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

import nltk.metrics
import nltk.classify.util
import nltk
from nltk.corpus import movie_reviews

def load(configProperties):


    nltk.download('movie_reviews')

    negids = movie_reviews.fileids('neg')
    posids = movie_reviews.fileids('pos')

    negfeats = [(word_feats(movie_reviews.words(fileids=[f])), 'neg') for f in negids]
    posfeats = [(word_feats(movie_reviews.words(fileids=[f])), 'pos') for f in posids]

    negcutoff = len(negfeats)*3/4
    poscutoff = len(posfeats)*3/4

    trainfeats = negfeats[:int(negcutoff)] + posfeats[:int(poscutoff)]
    testfeats = negfeats[int(negcutoff):] + posfeats[int(poscutoff):]
    test = 'train on %d instances, test on %d instances' % (len(trainfeats), len(testfeats))
    print(test)
    return trainfeats

def word_feats(words):
    return dict([(word, True) for word in words])
