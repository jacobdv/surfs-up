###############################################
# Set-Up + Data Connection
###############################################
from flask import Flask, jsonify
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

app = Flask(__name__)

engine = create_engine("sqlite:///Resources/hawaii.sqlite",echo=False)
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station

############################################### 
# Routes 
###############################################
# Home Page 
@app.route("/")
def homepage():
    return (
        f"Welcome to the Weather API for Honolulu, Hawaii!"
        f"</br></br>Currently available pages:"
        f"<ol><a href='/api/v1.0/precipitation'>Precipitation (/api/v1.0/precipitation)</a></ol>"
        f"<ol><a href='/api/v1.0/stations'>Stations (/api/v1.0/stations)</a></ol>"
        f"<ol><a href='/api/v1.0/tobs'>Temperatures (/api/v1.0/tobs)</a></ol>"
        #f"</br></br>User Input Required (Format: YYYY-MM-DD)"
        #f"<ol><a href='/api/v1.0/<start>'>Since Date (/api/v1.0/startdate)</a></ol>"
        #f"<ol><a href='/api/v1.0/<start>/<end>'>Between Dates (/api/v1.0/startdate/enddate)</a></ol>"
    )

# Precipitation
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    #return (
    #    f"Welcome to the Precipitation!"
    #)
    results = session.query(Measurement.date, Measurement.prcp).order_by(Measurement.date).all()
    session.close()

    all_results = []
    for item in results:
        item_dict = {}
        item_dict["Date"] = item[0]
        item_dict["Precipitation (inches)"] = item[1]
        all_results.append(item_dict)

    return jsonify(all_results)
    

# Stations
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    results = session.query(Station.station, Station.name).order_by(Station.name).all()
    session.close()

    all_results = []
    for item in results:
        item_dict = {}
        item_dict["Station ID"] = item[0]
        item_dict["Station Name"] = item[1]
        all_results.append(item_dict)

    return jsonify(all_results)

# Temperatures
@app.route("/api/v1.0/tobs")
def temperatures():
    session = Session(engine)
    ma = 'USC00519281' # Most Active Station ID from ipynb Analysis
    results = session.query(Measurement.date, Measurement.tobs).order_by(Measurement.date).filter(Measurement.station == ma).all()
    session.close()

    all_results = []
    for item in results:
        item_dict = {}
        item_dict["Date"] = item[0]
        item_dict["Temperature (°F)"] = item[1]
        all_results.append(item_dict)

    return jsonify(all_results)
    

# Since Date
# Between Date

if __name__ == "__main__":
    app.run(debug=True)