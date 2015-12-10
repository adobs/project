import os

parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parentdir)

from model import Profile, Location, db, connect_to_db
import geocoder 

def geo_code():
    locations = db.session.query(Profile.location).filter(Profile.location!='Pacoima, CA', Profile.location!='Irvington, NJ').group_by(Profile.location).all()
    for location in locations:
        print "location is", location
        try:
            g = geocoder.google(location[0])
            lat, lng = g.latlng

            print lat, lng

            new_location = Location(location=location[0], latitude=lat, longitude=lng)
            db.session.add(new_location)
        except:
            continue

    db.session.commit()

if __name__ == "__main__":
    #connect db to app
    from flask_app import app
    connect_to_db(app)
    print "Connected to DB."

     #create the database
    db.create_all()
    geo_code()