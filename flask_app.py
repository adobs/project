from flask import Flask, request, render_template, redirect, flash, session, jsonify
from jinja2 import StrictUndefined
from model import Profile, Adjective, Location, db, connect_to_db
# from flask_debugtoolbar import DebugToolbarExtension
from selenium_okc import create_new_user
from sending_a_message import send_message
from signing_in import is_signed_in
import re
from calculate_word_count import calculate_word_count
from datetime import datetime
app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined

@app.route("/")
def home():
    """Home page"""


    return render_template("home.html")

@app.route("/", methods=["POST"])
def home_landing():
    """Home page"""


    return redirect("/")

@app.route("/new-user-form")
def new_user_form():
    """Registration form"""

    months = xrange(1,13)
    days = xrange(1,32)
    years = xrange(1997,1914,-1)

    return render_template("create_new_user_form.html", months=months, days=days, years=years)


@app.route("/new-user", methods=["POST"])
def create_a_new_user():
    """JSON - gets new user information and sends to OKC"""

    orientation = request.form.get("orientation")
    gender = request.form.get("gender")
    birthmonth = request.form.get("birthmonth")
    birthdate = request.form.get("birthdate")
    birthyear = request.form.get("birthyear")
    zipcode = request.form.get("zip")
    email = request.form.get("email")
    screenname = request.form.get("screenname")
    password = request.form.get("password")

    print orientation
    print birthmonth
    results = create_new_user(orientation, gender, birthmonth, birthdate, birthyear, zipcode, email, screenname, password)
    if results == "success":
        if is_signed_in(screenname, password) == "True":
            session["screenname"] = screenname
            session["password"] = password   
            flash("You have successfully created a new user")
    print results
    return results    


@app.route("/login")
def login_form():
    """Login page"""

    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    """JSON - Login page"""

    screenname = request.form.get("screenname")
    password = request.form.get("password")

    if is_signed_in(screenname, password) == "True":
        session["screenname"] = screenname
        session["password"] = password   
        flash("You have successfully logged in")

    return is_signed_in(screenname, password)


@app.route("/logout")
def logout():
    """Logout page"""

    session.clear()
    flash("You have been logged out")

    return redirect("/")


@app.route("/okcbot")
def bot_form():
    """Input text for bot to send"""


    return render_template("okcbot.html")




@app.route("/okcbot", methods=["POST"])
def bot():
    """Input text for bot to send"""

    minimum_age = int(request.form.get("minimum_age"))
    maximum_age = int(request.form.get("maximum_age"))
    location = request.form.get("location")
    radius = int(request.form.get("radius"))
    gentation = request.form.get("gentation")
    message = request.form.get("message")
    num = int(request.form.get("num"))

    print session["screenname"]
    print session["password"]

    result = send_message(session["screenname"], session["password"], minimum_age, maximum_age, location, radius, gentation, message, num)
    
    print result

    if result:
        return result
    else: 
        flash("Message(s) successfully sent")
        return ""

@app.route("/map")
def map():
    """Map page."""

    # adjectives = db.session.query(Adjective).all()
    # profile_locations = db.session.query(Profile.location).all()
    # json_compiled = {}
    # for entry in adjectives:

    #     json_compiled[entry.location]= {}
    #     json_compiled[entry.location]['lat']=entry.latitude
    #     json_compiled[entry.location]['lng']=entry.longitude
    #     json_compiled[entry.location]['adj']=entry.adjective
    #     json_compiled[entry.location]['count']=entry.count
    #     json_compiled[entry.location]['population']= profile_locations.count(tuple([entry.location]))
    

    return render_template("map3.html")

@app.route("/map-json")
def map_json():
    """Map page."""

    orientation = request.args.get("orientation")
    orientation = re.sub('orientation=','',orientation)
    orientation_list = re.split('&',orientation)
    gender = request.args.get("gender")
    gender = re.sub('gender=','',gender)
    gender = re.sub('\+',' ',gender)
    gender_list = re.split('&',gender)
    age = request.args.get("age")
    age_list = re.split(' \- ',age)

    locations = db.session.query(Profile.location).all()

    locations = list(set(locations))

    for i in range(10-len(orientation_list)):
        orientation_list.append("None")

    # print "orientationlist is", orientation_list

    orientation0, orientation1, orientation2, orientation3, orientation4, orientation5, orientation6, orientation7, orientation8, orientation9 = orientation_list 

    for i in range(16-len(gender_list)):
        gender_list.append("None")

    # print "gender_list is", gender_list 

    gender0, gender1, gender2, gender3, gender4, gender5, gender6, gender7, gender8, gender9, gender10, gender11, gender12, gender13, gender14, gender15 = gender_list

    age_min, age_max = int(age_list[0]), int(age_list[1])

    compiled = {}
    i=0
    for location in locations:
        print "location", location, "is of type", type(location)
        print "location[0] =", location[0]
        #returns a list of tuples
        adjective_list = db.session.query(Adjective.adjectives).join(Profile).filter(db.or_(
            Profile.orientation.like('%'+orientation0+'%'), 
            Profile.orientation.like('%'+orientation1+'%'),
            Profile.orientation.like('%'+orientation2+'%'),
            Profile.orientation.like('%'+orientation3+'%'),
            Profile.orientation.like('%'+orientation4+'%'),
            Profile.orientation.like('%'+orientation5+'%'),
            Profile.orientation.like('%'+orientation6+'%'),
            Profile.orientation.like('%'+orientation7+'%'),
            Profile.orientation.like('%'+orientation8+'%'),  
            Profile.orientation.like('%'+orientation9+'%'))).filter(db.or_(
                Profile.gender.like('%'+gender0+'%'),
                Profile.gender.like('%'+gender1+'%'),
                Profile.gender.like('%'+gender2+'%'),
                Profile.gender.like('%'+gender3+'%'),
                Profile.gender.like('%'+gender4+'%'),
                Profile.gender.like('%'+gender5+'%'),
                Profile.gender.like('%'+gender6+'%'),
                Profile.gender.like('%'+gender7+'%'),
                Profile.gender.like('%'+gender8+'%'),
                Profile.gender.like('%'+gender9+'%'),
                Profile.gender.like('%'+gender10+'%'),
                Profile.gender.like('%'+gender11+'%'),
                Profile.gender.like('%'+gender12+'%'),
                Profile.gender.like('%'+gender13+'%'),
                Profile.gender.like('%'+gender14+'%'),
                Profile.gender.like('%'+gender15+'%'))).filter(Profile.age >= age_min).filter(Profile.age <= age_max).filter(Profile.location == location[0]).all()

        print "adjective list is", adjective_list
        
        if adjective_list:
            population = len(adjective_list)

            adjective, count = calculate_word_count(adjective_list)

            latitude = db.session.query(Location.latitude).filter(Location.location==location).one()[0]
            longitude = db.session.query(Location.longitude).filter(Location.location==location).one()[0]

            print "latitude is",latitude,"of type", type(latitude)


            location = location[0]
            compiled[location]= {}
            compiled[location]['lat']=latitude
            compiled[location]['lng']=longitude
            compiled[location]['adj']=adjective
            compiled[location]['count']=count
            compiled[location]['population']= population

            i+=1
            if i %10 == 0:
                print i, datetime.utcnow()
            # print adjective_list

            print "ORIENTATION IS", orientation
            print gender_list
            print age_list

            print compiled

    return jsonify(compiled)

if __name__ == "__main__":
    app.debug = True
    connect_to_db(app)

    # DebugToolbarExtension(app)
    app.run()