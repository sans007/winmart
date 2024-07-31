import numpy as np
import pandas as pd
from flask_cors import CORS
from flask import Flask, request, jsonify, render_template
from config import Config

from notebook.model.prediction import Prediction

def create_app():

    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)


    @app.route("/")
    def loadPage():
        return render_template("index.html", query="")


    @app.route("/api/submit", methods=["POST"])
    def submit():

        data = request.get_json()

        new_data = {
            "Item_Identifier": data["Item_Identifier"],
            "Item_Weight": data["Item_Weight"],
            "Item_Fat_Content": data["Item_Fat_Content"],
            "Item_Visibility": data["Item_Visibility"],
            "Item_Type": data["Item_Type"],
            "Item_MRP": data["Item_MRP"],
            "Outlet_Identifier": data["Outlet_Identifier"],
            "Outlet_Establishment_Year": data["Outlet_Establishment_Year"],
            "Outlet_Size": data["Outlet_Size"],
            "Outlet_Location_Type": data["Outlet_Location_Type"],
            "Outlet_Type": data["Outlet_Type"],
        }



        data_predic = Prediction(new_data)

        return jsonify(data_predic)
    
    return app


