from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets('MNIST_data', one_hot=True)

import cv

import tensorflow as tf
sess = tf.InteractiveSession()

sm = cv.Softmax(sess)
saver = tf.train.Saver()

# Training
y_ = tf.placeholder(tf.float32, shape=[None, 10])
cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y_, logits=sm.y))
train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)
for _ in range(1000):
	batch = mnist.train.next_batch(100)
	train_step.run(feed_dict={sm.x: batch[0], y_: batch[1]})

save_path = saver.save(sess, 'model/model.ckpt')
print("Model saved in file: %s" % save_path)