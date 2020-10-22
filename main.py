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

@app.route('/training')
def training():
  return render_template('training.html')


@app.route('/saveData/', methods=['POST'])
def save_data():
  global cond1, cond2, checking_cond1, prev_state, curr_state, mistake_count, success_count, flag, start_index, end_index, feedback, sound_file
  data = request.get_json()
  val_list = ['andang',0, 0, 0, 0]
  if data['type-exercise'] == 'bicep_curls':
    val_list[1] = data['count']
  elif data['type-exercise'] == 'front_raise':
    val_list[2] = data['count']
  elif data['type-exercise'] == 'lateral_raise':
    val_list[3] = data['count']
  elif data['type-exercise'] == 'squat':
    val_list[4] = data['count']

  with sqlite3.connect("database.db") as con:
    cur = con.cursor()
    cur.execute("INSERT INTO record(user, bicep_curls, front_raise, lateral_raise, squat) VALUES (?,?,?,?,?)",(val_list))
    con.commit()
  print('saved')

  cond1 = np.array([])
  cond2 = np.array([])
  prev_state = -1
  curr_state = -1
  success_count = 0
  mistake_count = 0
  flag = -1
  checking_cond1 = []
  start_index = 0
  end_index = 1
  feedback = ''
  sound_file = 'none'
  side = 'left'
  return ({'save':1})

@app.route('/predict/', methods=['POST'])
def predict():
  data = request.get_json()
  print(data)
  result = jsonify({'word':'A'})
  return result

if __name__ == '__main__':
  app.run(host='localhost', port=5000, debug=True)


