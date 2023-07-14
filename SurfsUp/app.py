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
Measurement = Base.classes.measurement
Station = Base.classes.station

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
        f"Welcome to the Climate API!</br>"
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
    one_year = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date <= '2017-08-23', Measurement.date >= '2016-08-23')
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
    all_results = session.query(Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation).all()
    session.close()
    all_stations = []
    for station, name, latitude, longitude, elevation in all_results:
        station_dictionary = {}
        station_dictionary['station'] = station
        station_dictionary['name'] = name
        station_dictionary['latitude'] = latitude
        station_dictionary['longitude'] = longitude
        station_dictionary['elevation'] = elevation
        all_stations.append(station_dictionary)
    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    most_active_station = session.query(Measurement.tobs).filter(Measurement.date <= '2017-08-18', Measurement.date >= '2016-08-18').filter(Measurement.station == 'USC00519281').all()
    session.close()
    most_active = list(np.ravel(most_active_station))
    return jsonify(most_active)

@app.route("/api/v1.0/<start>")
def start_temp(start):
    session = Session(engine)
    results = session.query(func.min(Measurement.tobs), 
                            func.max(Measurement.tobs), 
                            func.avg(Measurement.tobs)).filter(Measurement.date >= start).all()
    session.close()
    results_dictionary = {}
    results_dictionary["min_temp"] = results[0][0]
    results_dictionary["max_temp"] = results[0][1]
    results_dictionary["avg_temp"] = results[0][2]
    return jsonify(results_dictionary)

@app.route("/api/v1.0/<start>/<end>")
def start_end_temp(start, end):
    session = Session(engine)
    results = session.query(func.min(Measurement.tobs), 
                            func.max(Measurement.tobs), 
                            func.avg(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    session.close()
    results_dictionary = {}
    results_dictionary["min_temp"] = results[0][0]
    results_dictionary["max_temp"] = results[0][1]
    results_dictionary["avg_temp"] = results[0][2]
    return jsonify(results_dictionary)

if __name__ == "__main__":
    app.run(debug=True)