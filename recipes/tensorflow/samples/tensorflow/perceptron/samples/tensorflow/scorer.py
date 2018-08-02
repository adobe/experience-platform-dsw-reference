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

from ml.runtime.tensorflow.Interfaces.AbstractScorer import AbstractScorer
import tensorflow as tf
import numpy


class Scorer(AbstractScorer):
    def score(self, config={}):
        print("Executed scorer 2")
        print(config["modelPATH"])
        print(config["logsPATH"])
        with tf.Session() as sess:
            saver = tf.train.import_meta_graph(config["modelPATH"]+'/my_test_model-1000.meta')
            saver.restore(sess, tf.train.latest_checkpoint(config["modelPATH"]+'/'))
            graph = tf.get_default_graph()
            # Testing example, as requested (Issue #2)
            test_X = numpy.asarray([6.83, 4.668, 8.9, 7.91, 5.7, 8.7, 3.1, 2.1])
            X = tf.placeholder("float")
            W = graph.get_tensor_by_name("weight:0")
            b = graph.get_tensor_by_name("bias:0")
            pred = tf.add(tf.multiply(X, W), b)
            p = sess.run(pred,feed_dict={X:test_X})
            print(p)
