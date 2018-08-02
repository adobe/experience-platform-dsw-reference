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

from ml.runtime.tensorflow.Interfaces.AbstractTrainer import AbstractTrainer
import tensorflow as tf
import numpy


class Trainer(AbstractTrainer):
    def __init__(self):
        self.rng = numpy.random

    def train(self, config={}):
        print("Executed trainer 2")
        print(config["modelPATH"])
        print(config["logsPATH"])
        learning_rate = 0.01
        training_epochs = 1000
        display_step = 50

        # Training Data
        train_X = numpy.asarray([3.3, 4.4, 5.5, 6.71, 6.93, 4.168, 9.779, 6.182, 7.59, 2.167,7.042, 10.791, 5.313, 7.997, 5.654, 9.27, 3.1])
        train_Y = train_X*3+4
        n_samples = train_X.shape[0]

        # tf Graph Input
        X = tf.placeholder("float")
        Y = tf.placeholder("float")

        # Set model weights
        W = tf.Variable(self.rng.randn(), name="weight")
        b = tf.Variable(self.rng.randn(), name="bias")
        self.variable_summaries(W)
        self.variable_summaries(b)
        # Construct a linear model
        pred = tf.add(tf.multiply(X, W), b)

        # Mean squared error
        cost = tf.reduce_sum(tf.pow(pred - Y, 2)) / (2 * n_samples)
        self.variable_summaries(cost);
        # Gradient descent
        #  Note, minimize() knows to modify W and b because Variable objects are trainable=True by default
        optimizer = tf.train.GradientDescentOptimizer(learning_rate).minimize(cost)

        # Initialize the variables (i.e. assign their default value)
        init = tf.global_variables_initializer()
        saver = tf.train.Saver()
        # Run the initializer
        with tf.Session() as sess:
            sess.run(init)
            merged = tf.summary.merge_all()
            train_writer = tf.summary.FileWriter(config["logsPATH"],
                                                 sess.graph)
            # Fit all training data
            for epoch in range(training_epochs):
                for (x, y) in zip(train_X, train_Y):
                    summary, _ = sess.run([merged,optimizer], feed_dict={X: x, Y: y})
                    train_writer.add_summary(summary)
                # Display logs per epoch step
                if (epoch+1) % display_step == 0:
                    summary, c = sess.run([merged,cost], feed_dict={X: train_X, Y:train_Y})
                    train_writer.add_summary(summary)
                    print("Epoch:", '%04d' % (epoch+1), "cost=", "{:.9f}".format(c), \
                        "W=", sess.run(W), "b=", sess.run(b))
            saver.save(sess, config["modelPATH"] + '/my_test_model', global_step=1000)
            print("Optimization Finished!")
            training_cost = sess.run(cost, feed_dict={X: train_X, Y: train_Y})
            print("Training cost=", training_cost, "W=", sess.run(W), "b=", sess.run(b), '\n')

    def variable_summaries(self, var):
        with tf.name_scope('summaries'):
            mean = tf.reduce_mean(var)
            tf.summary.scalar('mean', mean)
            with tf.name_scope('stddev'):
                stddev = tf.sqrt(tf.reduce_mean(tf.square(var - mean)))
            tf.summary.scalar('stddev', stddev)
            tf.summary.scalar('max', tf.reduce_max(var))
            tf.summary.scalar('min', tf.reduce_min(var))
            tf.summary.histogram('histogram', var)
