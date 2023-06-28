# Import the dependencies.
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation</br>"
        f"/api/v1.0/stations</br>"
        f"/api/v1.0/tobs</br>"
        f"/api/v1.0/<start></br>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    one_year = session.query(measurement.date, measurement.prcp).filter(measurement.date <= '2017-08-23', measurement.date >= '2016-08-23')
    session.close()

    all_precipitation = []
    for date, prcp in one_year:
        results_dict = {}
        results_dict["date"] = date
        results_dict["prcp"] = prcp
        all_precipitation.append(results_dict)
    return jsonify(all_precipitation)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    results = session.query(station.station).all()
    session.close()
    all_stations = list(np.ravel(results))
    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    most_active_station = session.query(measurement.tobs).filter(measurement.date <= '2017-08-18', measurement.date >= '2016-08-18').filter(measurement.station == 'USC00519281').all()
    session.close()
    most_active = list(np.ravel(most_active_station))
    return jsonify(most_active)

@app.route("/api/v1.0/<start>")
def start(start):
    session = Session(engine)
    date = session.query(measurement.date)
    if date == start:
        start_date = session.query(measurement.date).filter(measurement.date > start).all()
        station_results = [func.min(measurement.tobs),
                           func.max(measurement.tobs),
                           func.avg(measurement.tobs)]
        station_results_list = session.query(*station_results).filter(measurement.date == start_date).all()
        station_results_list_2 = list(np.ravel(station_results_list))
        return jsonify(station_results_list_2)

    return jsonify({"error": f"{start} not found"}), 404

# @app.route("/api/v1.0/<start>/<end>")
# def start(start_end):

if __name__ == "__main__":
    app.run(debug=True)