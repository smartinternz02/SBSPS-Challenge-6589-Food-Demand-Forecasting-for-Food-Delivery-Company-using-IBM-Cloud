import requests
import numpy as np
from flask import Flask,redirect,url_for,render_template,request

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "wbMyju3RqkBQVhaRuxj_5XUVLjMnm0mIgnJIUum-DzK1"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

# NOTE: manually define and pass the array(s) of values to be scored in the next line


app = Flask(__name__)

@app.route("/",methods=['GET','POST'])
def index():
    return render_template("home.html")

@app.route("/home",methods=['GET','POST'])
def home():
    return render_template("home.html")
        
@app.route("/pred",methods=['GET','POST'])
def page():
    return render_template("upload.html")
@app.route("/predict",methods=['GET','POST'])
def predict():
    input_features=[float(x) for x in request.form.values()]
    print("Input Features are taken")
    features_value=[np.array(input_features)]
    print(features_value)
    features_name=['homepage_featured','emailer_for_promotion','op_area','cuisine','city_code','region_code','category']
    payload_scoring = {"input_data": [{"field":[features_name] , "values": [input_features]}]}
    response_scoring = requests.post('https://eu-gb.ml.cloud.ibm.com/ml/v4/deployments/7e639601-1078-43f5-982d-5500b54b47bc/predictions?version=2021-11-30', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
    predictions=response_scoring.json()
    output=predictions['predictions'][0]['values'][0][0]
    return render_template("upload.html",prediction_text=output)
if __name__ == "__main__":
    app.run()