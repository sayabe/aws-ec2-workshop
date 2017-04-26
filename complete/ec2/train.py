from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets('MNIST_data', one_hot=True)

import conv

import tensorflow as tf
sess = tf.InteractiveSession()

cnn = conv.Conv(sess)
saver = tf.train.Saver()

# Training
y_ = tf.placeholder(tf.float32, shape=[None,10])
cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y_, logits=cnn.y))
train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)
correct_prediction = tf.equal(tf.argmax(cnn.y, 1), tf.argmax(y_, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
sess.run(tf.global_variables_initializer())
for i in range(20000):
	batch = mnist.train.next_batch(50)
	if i%100 == 0:
		train_accuracy = accuracy.eval(feed_dict={
			cnn.x: batch[0], y_: batch[1], cnn.keep_prob: 1.0})
		print("step %d, training accuracy %g"%(i, train_accuracy))
	train_step.run(feed_dict={cnn.x: batch[0], y_: batch[1], cnn.keep_prob: 0.5})

print("test accuracy %g"%accuracy.eval(feed_dict={
	cnn.x: mnist.test.images, y_: mnist.test.labels, cnn.keep_prob: 1.0}))

save_path = saver.save(sess, 'model/model.ckpt')
print("Model saved in file: %s" % save_path)
