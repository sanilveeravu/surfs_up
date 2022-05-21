import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
#from sqlalchemy.orm import Session
from sqlalchemy.orm import relationship,scoped_session,sessionmaker,aliased
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#DB Init
engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine,reflect=True)

#Session = scoped_session(sessionmaker(bind=engine))
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

#DB Classes
Measurement = Base.classes.measurement
Station = Base.classes.station

#Flast init
app = Flask(__name__)
app.session = scoped_session(SessionLocal)
#session = Session(engine)

#Welcome Route
@app.route("/")
def welcome():
  return(
    '''
    Welcome to the Climate Analysis API!<br>
    Available Routes:<br>
    /api/v1.0/precipitation<br>
    /api/v1.0/stations<br>
    /api/v1.0/tobs<br>
    /api/v1.0/temp/start/end<br>
    ''')

#precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
  prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
  precipitation = session.query(Measurement.date, Measurement.prcp).\
      filter(Measurement.date >= prev_year).all()
  precip = {date: prcp for date, prcp in precipitation}
  return jsonify(precip)

#station route
@app.route("/api/v1.0/stations")
def stations():
  results = app.session.query(Station.station).all()  
  stations = list(np.ravel(results))
  return jsonify(stations=stations)

#temp route
@app.route("/api/v1.0/tobs")
def temp_monthly():
  prev_year = dt.date(2017,8,23) - dt.timedelta(days=365)
  results = session.query(Measurement.tobs).\
               filter(Measurement.date >= prev_year).\
               filter(Measurement.station == 'USC00519281').all() 
  temps = list(np.ravel(results))
  return jsonify(temps=temps)

#statistics data
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):
  sel = [func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)]  
  if not end:
    results = session.query(*sel).\
      filter(Measurement.date >= start).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

  results = session.query(*sel).\
     filter(Measurement.date >= start).\
     filter(Measurement.date <= end).all() 
  temps = list(np.ravel(results))
  return jsonify(temps=temps)

if __name__ == "__main__":
    app.run(debug=True)
