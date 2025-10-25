from flask import Flask, render_template, request,jsonify 

import numpy as np

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/write', methods=['GET', 'POST'])
def write():
   
    return render_template('write.html')

@app.route('/detect', methods=['GET', 'POST'])
def detect():
   
   return render_template('detect.html')

if __name__ == '__main__':
    app.run(debug=True,port =5001)