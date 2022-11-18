import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle

import inputSc

#load model
app = Flask(__name__)
model = pickle.load(open("RCforest.pkl", 'rb'))

#Redirects to the page to give the user input URL.
@app.route('/')
def predict():
    return render_template('index.html',result="")

#Fetches the URL given by the URL and passes to inputScript
@app.route('/',methods=['POST'])
def y_predict():
    '''
    For rendering results on HTML GUI
    '''
    url = request.form['url']
    checkprediction = inputSc.main(url)
    print(url)
    print(checkprediction)
    prediction = model.predict(X=checkprediction)
    print(prediction)
    output=prediction[0]
    print(output)
    if(output==1):
        pred="Your are safe!!  This is a Legal Website."
        
    else:
        pred=" Be cautious!!!! Not trusted"
    return render_template('index.html', result=pred,url=url)

#Takes the input parameters fetched from the URL by inputScript and returns the predictions
@app.route('/predict_api',methods=['POST'])
def predict_api():
    '''
    For direct API calls trought request
    '''
    data = request.get_json(force=True)
    prediction = model.predict([np.array(list(data.values()))])

    output = prediction[0]
    return jsonify(output)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)