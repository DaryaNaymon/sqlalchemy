from flask import Flask, jsonify 
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
import pandas as pd
Base = automap_base()
# create engine to hawaii.sqlite
engine = create_engine(r"sqlite:///C:\Users\Public\Challenge 10\Instructions\Resources\hawaii.sqlite")
# reflect an existing database into a new model
Base.metadata.create_all(engine)
# reflect the tables
Base.prepare(autoload_with=engine)
# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station
session = Session(engine)
app = Flask(__name__)
@app.route("/")
def home ():
    return "/api/v1.0/precipitation<br>/api/v1.0/stations<br>/api/v1.0/tobs<br>/api/v1.0/&lt;start&gt;<br>/api/v1.0/&lt;start&gt;/&lt;end&gt;"
@app.route("/api/v1.0/precipitation")
def pcpr ():
    session.query(measurement.date).order_by(measurement.date.desc()).first()
        # Calculate the date one year from the last date in data set.
    import datetime as dt
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    print("Query Date: ", query_date)

    # Perform a query to retrieve the data and precipitation scores

    session.query(measurement.date, measurement.prcp).\
        filter(measurement.date >= query_date)
    # Save the query results as a Pandas DataFrame and set the index to the date column
    df=pd.read_sql(session.query(measurement.date, measurement.prcp).\
        filter(measurement.date >= query_date).statement,session.bind)
    df
    # Sort the dataframe by date
    df=df.set_index("date")
    df=df.to_dict()
    return jsonify(df)
@app.route("/api/v1.0/stations")
def stations ():
    df=pd.read_sql(session.query(measurement.station).group_by(measurement.station).statement,session.bind)
    df=df.iloc[:,0].tolist()
    return jsonify(df)
@app.route("/api/v1.0/tobs")
def tobs ():
    import datetime as dt
    query_station = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    df=pd.read_sql(session.query(measurement.tobs).\
        filter(measurement.date >= query_station).filter(measurement.station == "USC00519281").statement,session.bind)
    df=df.to_dict()
    return jsonify(df)
@app.route("/api/v1.0/<start>")
def get_start (start):
    import datetime as dt
    start_time=dt.datetime.strptime(start,"%m-%d-%Y").date()
    df=pd.read_sql(session.query(func.max(measurement.tobs),func.min(measurement.tobs),func.avg(measurement.tobs)).\
        filter(measurement.date >= start_time).statement,session.bind)
    df=df.iloc[0,:].tolist()
    return jsonify(df)
@app.route("/api/v1.0/<start>/<end>")
def get_end (start,end):
    import datetime as dt
    start_time=dt.datetime.strptime(start,"%m-%d-%Y").date()
    end_time=dt.datetime.strptime(end,"%m-%d-%Y").date()
    df=pd.read_sql(session.query(func.max(measurement.tobs),func.min(measurement.tobs),func.avg(measurement.tobs)).\
        filter(measurement.date >= start_time).filter(measurement.date <= end_time).statement,session.bind)
    
    df=df.iloc[0,:].tolist()
    return jsonify(df)
