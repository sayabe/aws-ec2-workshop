import tensorflow as tf
import numpy as np
import cv

from flask import Flask, request, jsonify
app = Flask(__name__)

sess = tf.InteractiveSession()
classifier = cv.load_softmax(sess, 'model/model.ckpt')

@app.route('/')
def hello_world():
    return 'Hello from flask'

### TODO: Add /classify route ###

# @app.route('/classify', methods=['POST'])
# def classify():
#     x = np.array(request.json, dtype=np.uint8)
#     y = classifier.classify(x)
#     return jsonify(y.flatten().tolist())

if __name__ == '__main__':
    app.run()