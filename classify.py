# -*- coding: utf-8 -*-
"""
Created on Thu Nov 28 18:11:23 2019

@author: User
"""

from flask import Flask, request, render_template, flash, redirect, url_for
from fastai.vision import *


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join('C:\\', 'Users', 'User', 'Documents', 'snakes', 'uploads')


def cnn_work(img):
    learn = load_learner(Path(__file__).parent, 'export.pkl')

    pred_class, pred_idx, outputs = learn.predict(img)
    return pred_class


@app.route('/', methods=['GET', 'POST'])
def classify():
    res = ''
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            img = open_image(file_path)
            res = cnn_work(img)
        
    return render_template('form.html', result=res)


@app.route('/upload', methods=['POST'])
def upload():
    # check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)


if __name__ == '__main__':
    app.run()
