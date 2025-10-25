import base64
from flask import Flask, render_template, request,jsonify 
import base64
import re 
import joblib
import numpy as np
model = joblib.load('E:/Simple_Letter_Detection_ML/KNN_digits.sav') 
from PIL import Image

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/write', methods=['GET', 'POST'])
def write():
   
    return render_template('write.html')


@app.route('/detect', methods=['GET', 'POST'])
def detect():
    if request.method != 'POST':
        return jsonify(message='Send POST JSON {"image": "<dataURL>"}'), 200

    try:
        data = request.get_json(force=True)
        if not data or 'image' not in data:
            return jsonify(error='missing image field'), 400

        img_data_url = data['image']
        # extract base64 payload
        if ',' in img_data_url:
            b64 = img_data_url.split(',', 1)[1]
        else:
            b64 = img_data_url

        image_bytes = base64.b64decode(b64)
        with open('output.png', 'wb') as f:
            f.write(image_bytes)

        # open, convert and resize to model input (8x8)
        im = Image.open('output.png').convert('L')
        im = im.resize((8, 8), Image.LANCZOS)
        arr = np.array(im).astype(np.float32)

        # normalize/invert to match sklearn digits (0..16)
        arr = 255.0 - arr
        arr = (arr / 255.0) * 16.0
        features = arr.flatten().reshape(1, -1)

        prediction = model.predict(features)

        confidence = None
        if hasattr(model, 'predict_proba'):
            probs = model.predict_proba(features)
            try:
                class_index = list(model.classes_).index(prediction[0])
                confidence = float(probs[0][class_index])
            except Exception:
                confidence = float(np.max(probs))

        return jsonify(letter=str(int(prediction[0])), confidence=confidence)

    except Exception as e:
        return jsonify(error=str(e)), 500

 
def parseImage(imgData):
    imgstr = re.search(b'base64,(.*)', imgData).group(1)
    with open('output.png', 'wb') as output:
        output.write(base64.b64decode(imgstr))

if __name__ == '__main__':
    app.run(debug=True,port =5001)