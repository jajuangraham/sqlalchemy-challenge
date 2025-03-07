# Import the dependencies.
import numpy as np
import datetime as dt
import sqlalchemy

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine 

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################

# Create engine using the `hawaii.sqlite` database file
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")
# Declare a Base using `automap_base()`
Base = automap_base()
# Use the Base class to reflect the database tables
Base.prepare(autoload_with=engine)

# Assign the measurement class to a variable called `Measurement` and
# the station class to a variable called `Station`
Station = Base.classes.station
Measurement = Base.classes.measurement

# Create a session
Session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
@app.route('/')
def home():
    return (
        f"Welcome to the Climate Analysis!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;"
    )

# Define the precipitation route
@app.route('/api/v1.0/precipitation')
def precipitation():
    #
    Last_Date = dt.date(*map(int, Recent_Date[0].split('-'))) - dt.timedelta(days=365)

    
    Precipitation= Session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= Last_Date).all()

   
    Precipitation_dict = {date: prcp for date, prcp in Precipitation}

    return jsonify(Precipitation_dict)

# Define the  route
@app.route('/api/v1.0/stations')
def stations():

    s_data = Session.query(Station.station).all()

    s_list = [station[0] for station in s_data]

    return jsonify(s_list)

# Define the route
@app.route('/api/v1.0/tobs')
def tobs():
   
    data = Session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= Temp).all()

    
    temperature_dict = [{'date': date, 'temperature': tobs} for date, tobs in data]

    return jsonify(temperature_dict)

# Define the start and start/end routes
@app.route('/api/v1.0/<start>')
@app.route('/api/v1.0/<start>/<end>')
def temperature_stats(start, end=None):
    
    if end:
        stats_data = Session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    else:
        stats_data = Session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date >= start).all()

   
    stats_list = [{'min_temperature': stats[0], 'avg_temperature': stats[1], 'max_temperature': stats[2]} for stats in stats_data]

    return jsonify(stats_list)

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)