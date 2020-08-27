#import dependancies
import numpy as np 
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

#reference to measurements and station
Measurement =Base.classes.measurement
Station = Base.classes.station

#create app
app = Flask(__name__)

#create home page
@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return (
    	f"Welcome to the Hawaii Climate API! <br/>"
    	f"Available Routes:<br/>"
    	f"/api/v1.0/precipitation<br/>"
    	f"/api/v1.0/stations<br/>"
    	f"/api/v1.0/tobs<br/>"
    	f"/api/v1.0/[start_date]<br/>"
    	f"Enter start date in YYYY-MM-DD format. This will give you Min, Max and Average temp for given time period<br/>"
    	f"/api/v1.0/[start-date]/[end_date]<br/>"
    	f"Enter start date and end date in YYYY-MM-DD format. This will give you Min, Max and Average temp for given time period"
    	)

#create precipitation page
@app.route("/api/v1.0/precipitation")
def precipitation():
	session =Session(engine)
	#query to get date and precipitation data
	results = session.query(Measurement.date, Measurement.prcp)

	session.close()

	all_precip = []
	precip_dict ={}
	for date, precip in results:
		precip_dict[date] = precip

	return jsonify(precip_dict)


#create station page
@app.route("/api/v1.0/stations")
def stations():
	session =Session(engine)
	#query to get station names
	results = session.query(Station.name).all()
	session.close()
	# Convert list of tuples into normal list
	all_names = list(np.ravel(results)) 
	return jsonify(all_names)


#create tobs page
@app.route("/api/v1.0/tobs")
def tobs():
	session =Session(engine)
	#query to get tobs data for most active station for the last year
	results = session.query(Measurement.tobs).filter(Measurement.station == 'USC00519281', Measurement.date >= '2016-08-23').all()
	session.close()
	# Convert list of tuples into normal list
	temps_over_a_year = list(np.ravel(results)) 
	return jsonify(temps_over_a_year)

#date start query
@app.route("/api/v1.0/<start>")
def start_date_temps(start):
	session=Session(engine)
	#query to get min, max, avg temps for start date and greater 
	highest_temp = session.query(func.max(Measurement.tobs)).filter(Measurement.date >= start.strip()).all()
	lowest_temp = session.query(func.min(Measurement.tobs)).filter(Measurement.date >= start.strip()).all()
	average_temp = session.query(func.avg(Measurement.tobs)).filter(Measurement.date >= start.strip()).all()
	session.close()
	temp_dict={}
	temp_dict['Max Temp']=highest_temp
	temp_dict['Min Temp']=lowest_temp
	temp_dict['Average Temp']=average_temp
	return jsonify(temp_dict)


#date start and end query
@app.route("/api/v1.0/<start>/<end>")
def date_range_temps(start, end):
	session=Session(engine)
	#query to get min, max, avg temps for start date and greater 
	highest_temp = session.query(func.max(Measurement.tobs)).filter(Measurement.date >= start.strip(),Measurement.date <= end.strip() ).all()
	lowest_temp = session.query(func.min(Measurement.tobs)).filter(Measurement.date >= start.strip(),Measurement.date <= end.strip() ).all()
	average_temp = session.query(func.avg(Measurement.tobs)).filter(Measurement.date >= start.strip(),Measurement.date <= end.strip() ).all()
	session.close()
	temp_dict={}
	temp_dict['Max Temp']=highest_temp
	temp_dict['Min Temp']=lowest_temp
	temp_dict['Average Temp']=average_temp
	return jsonify(temp_dict)



if __name__ == '__main__':
    app.run(debug=True)
