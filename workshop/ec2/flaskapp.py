import tensorflow as tf
import numpy as np
import conv

from flask import Flask, request, jsonify
app = Flask(__name__)

sess = tf.InteractiveSession()
cnn = conv.load(sess, 'model/model.ckpt')

@app.route('/')
def hello_world():
    return 'Hello from flask'

@app.route('/classify', methods=['POST'])
def classify():
    x = np.array(request.json, dtype=np.uint8)
    y = cnn.classify(x)
    visualize(x, 0.5)
    print(y)
    return jsonify(y.flatten().tolist())

def visualize(x, thres=0):
    x = np.reshape(x, [28, 28])
    for row in x:
        s = ''
        for col in row:
            if col > thres:
                s += '1'
            else:
                s += '.'
        print(s)

if __name__ == '__main__':
    app.run()