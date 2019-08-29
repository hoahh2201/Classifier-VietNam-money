from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import base64
import json
import tensorflow as tf
import numpy as np
import base64
import re
import cv
import matplotlib.pyplot as plt

app = Flask(__name__)
app.secret_key = 'lmao'

model = tf.keras.models.load_model("static/models/univer_model.h5")

def parse_image(imgData):
    print(imgData)
    imgstr = re.search(b"base64,(.*)", imgData).group(1)
    img_decode = base64.decodebytes(imgstr)
    with open("output.jpg", "wb") as file:
        file.write(img_decode)
    return img_decode

@app.route("/upload/", methods=["POST"])
def upload_file():
    img_raw = parse_image(request.get_data())
    image = tf.image.decode_jpeg(img_raw, channels=3)
    image = tf.image.resize(image, [192, 192])
    image = image / 255.0
    image = 2*image - 1
    print(image.shape)
    probabilites = model.predict(tf.expand_dims(image,0))
    prediction = np.argmax(probabilites, axis=1)[0]

    real_money = {0:'1,000', 3:'2,000', 6:'5,000', 1:'10,000', 4:'20,000', 7:'50,000', 2:'100,000', 5:'200,000', 8:'500,000'}
    return real_money[prediction]


@app.route('/')
def index():
	return render_template('frontend/index.html')


@app.route("/predict", methods = ["GET"])
def predict():
    return render_template('frontend/predict.html')


@app.route('/test/', methods=["GET", "POST"])
def abc_test():
    if request.method=='POST':
        print("It is a POST request")
        try:
            print(request.form['PHOTO'])
        except Exception as e:
            print(('exception 1:', e))
        try:
            print(request.files['PHOTO'])
        except Exception as e:
            print(('exception 2:', e))
        try:
            filename=photos.save(request.files['PHOTO'])
            print("filename")
            picture=unicode(filename)
            current_user.picture=picture
            db.session.commit()
            return redirect(url_for('abc_test'))
        except Exception as e:
            print(('exception 3:', e))
        return 'DID NOT SAVE IMAGE'
    print("did not POST")
    return render_template('abc_test.html')

if __name__ == '__main__':
	app.debug=1
	app.run()
