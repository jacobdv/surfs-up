###############################################
# Set-Up + Data Connection
###############################################
# Imports
from flask import Flask, jsonify
import numpy as np
import datetime as dt
import statistics as st
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# App and class creations.
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
    # Welcome message and links to available pages, with the url finish listed as well.
    return (
        f"Welcome to the Weather API for Honolulu, Hawaii!"
        f"</br></br>Currently available pages:"
        f"<ul><li><a href='/api/v1.0/precipitation'>Precipitation (/api/v1.0/precipitation)</a></li>"
        f"<li><a href='/api/v1.0/stations'>Stations (/api/v1.0/stations)</a></li>"
        f"<li><a href='/api/v1.0/tobs'>Temperatures (/api/v1.0/tobs)</a></li></ul>"
        f"</br></br>User Input Required (Format: YYYY-MM-DD)"
        f"<ul><li><a href='/api/v1.0/2010-01-01'>Since Date (/api/v1.0/start_date)</a></li>"
        f"<li><a href='/api/v1.0/2010-01-01/2017-08-23'>Between Dates (/api/v1.0/start_date/end_date)</a></li></ul>"
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
    # Error Handling - Making sure dates are within proper ranges for year, month and day.
    # Makes sure the start date is the right length.
    if len(start_date) != 10:
        return (
            "Hmmm, looks like your date is the wrong length. Remember the format is YYYY-MM-DD!"
        )
    # Makes sure the start year is within the range of years in the data.
    elif int(start_date[0:4]) < 2010 or int(start_date[0:4]) > 2017:
        return (
            "It looks like that year is outside the range of our data! Try a date between January 2010 and August 2017."
            "<br>Make sure to include the month and day too!"
        )
    # Checks that the given month is a valid month.
    elif int(start_date[5:7]) < 1 or int(start_date[5:7]) > 12:
        return (
            "Hmmm. Make sure you're entering a valid month. Remember the format is YYYY-MM-DD!"
        )
    # Checks that the given day is greater than 1.
    elif int(start_date[8:10]) < 1:
        return (
            "Hmmm. Make sure you're entering a valid day. Remember the format is YYYY-MM-DD!"
        )
    # Clears day values for February, accounting for Leap Years in 2012 and 2016.
    elif start_date[5:7] == '02':
        if int(start_date[8:10]) == 29:
            if int(start_date[0:4]) != 2012 and int(start_date[0:4]) != 2016:  
                return ("This isn't a Leap Year. Make sure you're using YYYY-MM-DD!")
        elif int(start_date[8:10]) > 29:
            return ("This isn't a valid day in February in any year! Make sure you're using YYYY-MM-DD!")

    # Runs standard query.
    try:
        # Creates a session and queries for the temperature for each date in the selected range.
        session = Session(engine)
        results = session.query(Measurement.tobs).\
            filter(Measurement.date >= start_date).order_by(Measurement.date).all()
        session.close()

        # Creates a new list from the results that doesn't include 'Null' values.
        temp_list = []
        for x in results:
            if x[0] != 'Null':
                temp_list.append(float(x[0]))

        # Calculates max, min, and average temperature.
        max_temp = max(temp_list)
        min_temp = min(temp_list)
        avg_temp = round(st.mean(temp_list),1)

    # Reminds user of proper date format if there is a value error, though this should be difficult with the above error handling.
    except ValueError:
        return (
            f"It appears you haven't entered a valid date. Please use YYYY-MM-DD format. Thanks!"
        )

    # Returns temperature data since the given start date.
    return (
        f"<u>Temperature Data Since {start_date}</u>"
        f"</br>Max Temperature:    {max_temp}°F"
        f"</br>Min Temperature:    {min_temp}°F"
        f"</br>Average Temperature:    {avg_temp}°F"
    )

# Between Date
@app.route("/api/v1.0/<start_date>/<end_date>")
def between_dates(start_date,end_date):
    if len(start_date) != 10 or len(end_date != 10):
        return (
            "Hmmm, looks like one of your dates is the wrong length. Remember the format is YYYY-MM-DD!"
        )
    elif int(start_date[0:4]) < 2010 or int(start_date[0:4]) > 2017 or int(end_date[0:4]) < 2010 or int(end_date[0:4]) > 2017:
        return (
            "It looks like that year is outside the range of our data! Try a date between January 2010 and August 2017."
            "<br>Make sure to include the month and day too!"
        )
    elif int(start_date[5:7]) < 1 or int(start_date[5:7]) > 12 or int(end_date[5:7]) < 1 or int(end_date[5:7]) > 12:
        return (
            "Hmmm. Make sure you're entering a valid month. Remember the format is YYYY-MM-DD!"
        )
    elif int(start_date[8:10]) < 1 or int(start_date[8:10]) > 31 or int(end_date[8:10]) < 1 or int(end_date[8:10]) > 31:
        return (
            "Hmmm. Make sure you're entering a valid day. Remember the format is YYYY-MM-DD!"
        )
    try:
        session = Session(engine)
        results = session.query(Measurement.tobs).\
            filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).\
                order_by(Measurement.date).all()
        session.close()

        temp_list = []
        for x in results:
            if x[0] != 'Null':
                temp_list.append(float(x[0]))

        max_temp = max(temp_list)
        min_temp = min(temp_list)
        avg_temp = round(st.mean(temp_list),1)
    except ValueError:
        if (int(start_date[0:4]) > int(end_date[0:4])) or\
        ((start_date[0:4] == end_date[0:4]) and (int(start_date[5:7]) > int(end_date[5:7]))) or\
        ((start_date[0:7] == end_date[0:7]) and (int(start_date[8:10]) > int(end_date[8:10]))):
            return (
                "Make sure your end date is after your start date. Remember the format is YYYY-MM-DD!"
            )
        else:
            return (
                f"It appears you haven't entered a valid date. Please use YYYY-MM-DD format. Thanks!"
            )
    return (
        f"<u>Temperature Data Between {start_date} and {end_date}</u>"
        f"</br>Max Temperature:    {max_temp}°F"
        f"</br>Min Temperature:    {min_temp}°F"
        f"</br>Average Temperature:    {avg_temp}°F"
    )

if __name__ == "__main__":
    app.run(debug=True)