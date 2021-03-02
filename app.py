###############################################
# Set-Up + Data Connection
###############################################
from flask import Flask, jsonify
import numpy as np
import datetime as dt
import statistics as st
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
# Static Routes 
###############################################
# Home Page 
@app.route("/")
def homepage():
    return (
        f"Welcome to the Weather API for Honolulu, Hawaii!"
        f"</br></br>Currently available pages:"
        f"<ol><a href='/api/v1.0/precipitation'>Precipitation (/api/v1.0/precipitation)</a></ol>"
        #f"<ol><a href='/api/v1.0/precipitation-grouped'>Precipitation: All Stations Grouped (/api/v1.0/precipitation-grouped)</a></ol>"
        f"<ol><a href='/api/v1.0/stations'>Stations (/api/v1.0/stations)</a></ol>"
        f"<ol><a href='/api/v1.0/tobs'>Temperatures (/api/v1.0/tobs)</a></ol>"
        f"</br></br>User Input Required (Format: YYYY-MM-DD)"
        f"<ol><a href='/api/v1.0/2010-01-01'>Since Date (/api/v1.0/startdate)</a></ol>"
        #f"<ol><a href='/api/v1.0/<start>/<end>'>Between Dates (/api/v1.0/startdate/enddate)</a></ol>"
    )

# Precipitation
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    one_year = dt.datetime(2016, 8, 23)
    results = session.query(Measurement.date, Measurement.prcp).\
        order_by(Measurement.date).filter(Measurement.date > one_year).all()
    session.close()

    all_results = []
    for item in results:
        item_dict = {}
        item_dict["Date"] = item[0]
        item_dict["Precipitation (inches)"] = item[1]
        all_results.append(item_dict)

    return jsonify(all_results)
    
# # Precipitation - Grouped
# @app.route("/api/v1.0/precipitation-grouped")
# def precipitation_grp():
#     session = Session(engine)
#     one_year = dt.datetime(2016, 8, 23)
#     results = session.query(Measurement.date, Measurement.prcp).group_by(Measurement.date).\
#         order_by(Measurement.date).filter(Measurement.date > one_year).all()
#     session.close()

#     all_results = []
#     for item in results:
#         item_dict = {}
#         item_dict["Date"] = item[0]
#         item_dict["Precipitation (inches)"] = item[1]
#         all_results.append(item_dict)

#     return jsonify(all_results)

# Stations
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    results = session.query(Station.station, Station.name).order_by(Station.name).all()
    session.close()

    all_results = []
    station_list = []
    for item in results:
        item_dict = {}
        item_dict["Station ID"] = item[0]
        item_dict["Station Name"] = item[1]
        all_results.append(item_dict)
        #station_list.append(item[1])
        station_list.append(item[0])

    return jsonify(station_list, all_results)

# Temperatures
@app.route("/api/v1.0/tobs")
def temperatures():
    session = Session(engine)
    one_year = dt.datetime(2016, 8, 23)
    ma = 'USC00519281' # Most Active Station ID from ipynb Analysis
    results = session.query(Measurement.date, Measurement.tobs).\
        order_by(Measurement.date).filter(Measurement.station == ma).\
            filter(Measurement.date > one_year).all()
    session.close()

    all_results = []
    for item in results:
        item_dict = {}
        item_dict["Date"] = item[0]
        item_dict["Temperature (°F)"] = item[1]
        all_results.append(item_dict)

    return jsonify(all_results)
    
############################################### 
# Dynamic Routes 
###############################################
# Since Date
@app.route("/api/v1.0/<start_date>")
def since_date(start_date):
    session = Session(engine)
    results = session.query(min(Measurement.tobs),max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).order_by(Measurement.date).all()
    session.close()
    
    all_results = []
    for item in results:
        item_dict = {}
        # Look for min max and average in for loop??????????????
        item_dict["Min Temperature (°F)"] = item[0]
        item_dict["Max Temperature (°F)"] = item[1]
        #item_dict["Average Temperature (°F)"] = item[2]
        all_results.append(item_dict)

    return jsonify(all_results)

# Between Date

if __name__ == "__main__":
    app.run(debug=True)