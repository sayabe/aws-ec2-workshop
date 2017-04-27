   import tensorflow as tf

def weight_variable(shape, name):
	initial = tf.truncated_normal(shape, stddev=0.1)
	return tf.Variable(initial, name=name)

def bias_variable(shape, name):
	initial = tf.constant(0.1, shape=shape)
	return tf.Variable(initial, name=name)

def conv2d(x, W):
	return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')

def max_pool_2x2(x):
	return tf.nn.max_pool(x, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')

def load_softmax(sess, model):
	sm = Softmax(sess)
	saver = tf.train.Saver()
	saver.restore(sess, model)
	return sm

def load_conv(sess, model):
	cnn = Conv(sess)
	saver = tf.train.Saver()
	saver.restore(sess, model)
	return cnn

class Classifier:

	def __init__(self, sess):
		self.sess = sess
		self.y = self.build_graph()
		sess.run(tf.global_variables_initializer())

	def build_graph(self):
		pass

class Conv(Classifier):

	def __init__(self, sess):
		Classifier.__init__(self, sess)

	def build_graph(self):

		# Inputs
		self.x = tf.placeholder(tf.float32, shape=[None, 784])
		self.keep_prob = tf.placeholder(tf.float32)

		# Parameters
		W_conv1 = weight_variable([5, 5, 1, 32], 'W_conv1')
		b_conv1 = bias_variable([32], 'b_conv1')
		W_conv2 = weight_variable([5, 5, 32, 64], 'W_conv2')
		b_conv2 = bias_variable([64], 'b_conv2')
		W_fc1 = weight_variable([7*7*64, 1024], 'W_fc1')
		b_fc1 = bias_variable([1024], 'b_fc1')
		W_fc2 = weight_variable([1024, 10], 'W_fc2')
		b_fc2 = bias_variable([10], 'b_fc2')

		# Reshape vector into 2d image
		x_image = tf.reshape(self.x, [-1, 28, 28, 1])

		# First conv layer, 32 features, max pool
		h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1) + b_conv1)
		h_pool1 = max_pool_2x2(h_conv1)

		# Second conv layer, 64 features, max pool
		h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)
		h_pool2 = max_pool_2x2(h_conv2)

		# Flatten vector
		h_pool2_flat = tf.reshape(h_pool2, [-1, 7*7*64])

		# Densely connected layer
		h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)

		# Dropout layer
		h_fc1_drop = tf.nn.dropout(h_fc1, self.keep_prob)

		# Readout layer
		y = tf.matmul(h_fc1_drop, W_fc2) + b_fc2
		return y

	def classify(self, x, keep_prob=1.0):
		y_out = tf.argmax(self.y, 1)
		return self.sess.run(y_out, feed_dict={
			self.x: [x], self.keep_prob: keep_prob})

class Softmax(Classifier):

	def __init__(self, sess):
		Classifier.__init__(self, sess)

	def build_graph(self):

		# Inputs
		self.x = tf.placeholder(tf.float32, shape=[None, 784])

		# Parameters
		W = tf.Variable(tf.zeros([784, 10]), 'W')
		b = tf.Variable(tf.zeros([10]), 'b')

		return tf.matmul(self.x, W) + b

	def classify(self, x):
		y_out = tf.argmax(self.y, 1)
		return self.sess.run(y_out, feed_dict={
			self.x: [x]})

