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
    if request.method == 'POST':
        data = request.get_json() or {}
        image = data.get('image')
        if not image:
            return jsonify(error='no image provided'), 400
        # TODO: replace with real ML inference
        return jsonify(letter='?', confidence=0.0)
    return jsonify(message='POST JSON {"image": "<dataURL>"}')

if __name__ == '__main__':
    app.run(debug=True,port =5001)