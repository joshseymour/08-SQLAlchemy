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
        f"Welcome to the Precipitation API! <br/>"
        f"Below are your available routes: <br/>"
        f"/api/v1.0/precipitation <br/>"
        f"/api/v1.0/stations <br/>"
        f"/api/v1.0/tobs <br/>"
        f"/api/v1.0/start<start> <br/>"
        f"/api/v1.0/start/end/<start>/<end>"
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
        precipitation_dict["Date"] = date
        precipitation_dict["Participation"] = prcp
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

@app.route("/api/v1.0/start/<start>")
def temps(start):
    """TMIN, TAVG, and TMAX for a list of dates"""
    session = Session(engine)
    results = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date > start).group_by(Measurement.date).all()    
    # Create a dictionary from the row data and append to a list of all precipitation in date range  
    start_list = []
    for date in results:
        start_dict = {}
        start_dict["Date"] = date[0]
        start_dict["Min Temp"] = date[1]
        start_dict["Avg Temp"] = date[2]
        start_dict["Max Temp"] = date[3]
        start_list.append(start_dict)

    return jsonify(start_list)

@app.route("/api/v1.0/start/end/<start>/<end>")
def start_end(start, end):
    """TMIN, TAVG, and TMAX for a list of dates"""
    session = Session(engine)
    results = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date > start).filter(Measurement.date < end).group_by(Measurement.date).all()    
    
    start_list = []
    for date in results:
        start_dict = {}
        start_dict["Date"] = date[0]
        start_dict["Min Temp"] = date[1]
        start_dict["Avg Temp"] = date[2]
        start_dict["Max Temp"] = date[3]
        start_list.append(start_dict)
        session.commit()
    
    return jsonify(start_list)


if __name__ == "__main__":
    app.run(debug=False)
