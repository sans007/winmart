
import os
from flask import Flask,request,jsonify,render_template
import pickle
import numpy as np
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

model = pickle.load(open('./notebook/datapred.pkl', 'rb'))

@app.route("/")
def loadPage():
	return render_template('index.html', query="")

@app.route("/api/submit", methods = ['POST'])
def submit():

    data = request.get_json()


    new_data = {
        "Item_Identifier" : data["Item_Identifier"],
        "Item_Weight" : data["Item_Weight"],
        "Item_Fat_Content" : data["Item_Fat_Content"],
        "Item_Visibility" : data["Item_Visibility"],
        "Item_Type" : data["Item_Type"],
        "Item_MRP" : data["Item_MRP"],
        "Outlet_Identifier" : data["Outlet_Identifier"],
        "Outlet_Establishment_Year" : data["Outlet_Establishment_Year"],
        "Outlet_Size" : data["Outlet_Size"],
        "Outlet_Location_Type" : data["Outlet_Location_Type"],
        "Outlet_Type" : data["Outlet_Type"]
   }
    
    print("Received data:", data)

    # MODEL_PATH = r'./models/DataPred.pkl'
    
    # response = model(data)
    return jsonify(data)
    # return jsonify(response)


if __name__ == '__main__':
    app.run(port= 3000,debug=True)