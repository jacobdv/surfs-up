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
    results = session.query(Measurement.date, Measurement.tobs)
    test = list(np.ravel(results))
    return jsonify(test)
    session.close()

# Stations
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    return (
        f"Welcome to Stations!"
    )
    session.close()

# Temperatures
@app.route("/api/v1.0/tobs")
def temperatures():
    session = Session(engine)
    return (
        f"Welcome to Temperatures!"
    )
    session.close()

# Since Date
# Between Date

if __name__ == "__main__":
    app.run(debug=True)