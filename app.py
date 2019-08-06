import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Stations = Base.classes.station

# Create our session (link) from Python to the DB

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def home():
    return (
        f"Welcome to the Precipitation API!<br/>"
        f"Below are your available routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )
@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return the precipitation data as a dictionary and display in json"""
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.prcp).all()
        
        
    # Create a dictionary from the row data and append to a list of all precipitation
    all_precipitation = []
    for date, prcp in results:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["prcp"] = prcp
        all_precipitation.append(precipitation_dict)
    
    return jsonify(all_precipitation)

@app.route("/api/v1.0/stations")
def stations():
    """Return the stations as a json"""
    session = Session(engine)
    results = session.query(Stations.station).all()
        
    return jsonify(results)

@app.route("/api/v1.0/tobs")
def tobs():
    """Return the tempurature observations as a json"""
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date <= '2017-08-23').filter(Measurement.date > '2016-08-23').all()
        
    return jsonify(results)

@app.route("/api/v1.0/<start>")
def calc_temps(start_date, end_date):
    """TMIN, TAVG, and TMAX for a list of dates"""
    session = Session(engine)
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start_date).all()    
    
    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=False)
