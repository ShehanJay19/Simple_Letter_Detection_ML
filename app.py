from flask import Flask, render_template, request,jsonify 

import numpy as np

app = Flask(__name__)


@app.rouute('/')
def home():
    return render_template('index.html')

@app.route('/write')
def write():
    return render_template('write.html')
