from flask import Flask, render_template, render_template, request, jsonify

import numpy as np
import pandas as pd
import json
import sqlite3

from math import degrees
from random import choice
import tensorflow as tf
import numpy as np
import re
import os
import base64
import uuid



app = Flask(__name__)

@app.route('/')
def home():
  return render_template('home.html')
model = tf.keras.models.load_model("models/Sign_language_model.h5")
class_names = np.array(['A', 'B', 'C', 'D', 'E', 
                        'F', 'G', 'H', 'I','J','K','L','M',
                        'N','O','P','Q','R','S','T','U',
                        '1','2','3','4','5','6','7','8','9','0'])

@app.route('/training')
def training():
  return render_template('training.html')


# @app.route('/saveData/', methods=['POST'])
# def save_data():
#   global cond1, cond2, checking_cond1, prev_state, curr_state, mistake_count, success_count, flag, start_index, end_index, feedback, sound_file
#   data = request.get_json()
#   val_list = ['andang',0, 0, 0, 0]
#   if data['type-exercise'] == 'bicep_curls':
#     val_list[1] = data['count']
#   elif data['type-exercise'] == 'front_raise':
#     val_list[2] = data['count']
#   elif data['type-exercise'] == 'lateral_raise':
#     val_list[3] = data['count']
#   elif data['type-exercise'] == 'squat':
#     val_list[4] = data['count']

#   with sqlite3.connect("database.db") as con:
#     cur = con.cursor()
#     cur.execute("INSERT INTO record(user, bicep_curls, front_raise, lateral_raise, squat) VALUES (?,?,?,?,?)",(val_list))
#     con.commit()
#   print('saved')

#   cond1 = np.array([])
#   cond2 = np.array([])
#   prev_state = -1
#   curr_state = -1
#   success_count = 0
#   mistake_count = 0
#   flag = -1
#   checking_cond1 = []
#   start_index = 0
#   end_index = 1
#   feedback = ''
#   sound_file = 'none'
#   side = 'left'
#   return ({'save':1})
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
  # print(data)
  # result = jsonify({'word':'A'})
  # return result
  data = request.get_json()
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
  app.run(host='localhost', port=5000, debug=True)


