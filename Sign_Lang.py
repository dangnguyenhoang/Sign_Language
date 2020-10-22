from flask import Flask, render_template, render_template, request, jsonify
 
import tensorflow as tf
import numpy as np
import re
import os
import base64
import uuid
 
 
app = Flask(__name__)
 
@app.route('/')
def index():
    return render_template('home_page.html') 
 
 
model = tf.keras.models.load_model("models/vnd_classifier.h5")
class_names = np.array(['A', 'B', 'C', 'D', 'E', 
                        'F', 'G', 'H', 'I','J','K','L','M',
                        'N','O','P','Q','R','S','T','U'])
 
def parse_image(imgData):
    img_str = re.search(b"base64,(.*)", imgData).group(1)
    img_decode = base64.decodebytes(img_str)
    filename = "{}.jpg".format(uuid.uuid4().hex)
    with open('uploads/'+filename, "wb") as f:
        f.write(img_decode)
    return img_decode
 
def preprocess(image):
    image = tf.image.decode_jpeg(image, channels=3)
    image = tf.image.resize(image, [192, 192])
    # Use `convert_image_dtype` to convert to floats in the [0,1] range.
    image = tf.image.convert_image_dtype(image, tf.float32)
    image = (image*2) - 1  # normalize to [-1,1] range
    image = tf.image.per_image_standardization(image)
    return image
 
@app.route('/predict/', methods=['POST'])
def predict():
    data = request.get_json()
 
    # Preprocess the upload image
    img_raw = data['data-uri'].encode()
    image = parse_image(img_raw)
    image = preprocess(image)
    image = tf.expand_dims(image, 0)
 
    probs = model.predict(image)
    label = np.argmax(probs, axis=1)
    label = class_names[label[0]]
    probs = probs[0].tolist()
    probs = [(probs[i], class_names[i]) for i in range(len(class_names))]
 
    return jsonify({'label': label, 'probs': probs}) 
 
 
if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000, debug=True)