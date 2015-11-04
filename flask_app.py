from flask import Flask, request, render_template, redirect, flash, session, jsonify
from jinja2 import StrictUndefined
from model import Profile, Adjective, Gender, Orientation, UsernameOrientation, UsernameGender, Location, db, connect_to_db
# from flask_debugtoolbar import DebugToolbarExtension
from selenium_okc import create_new_user
from sending_a_message import send_message
from signing_in import is_signed_in
import re
from calculate_word_count import calculate_word_count
from datetime import datetime
from map_helper import get_joined_adjectives, get_lat_long, add_adjective_to_compiled, add_nothing_to_compiled

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
    
    if result:
        return result
    else: 
        flash("Message(s) successfully sent")
        return ""

@app.route("/map")
def map():
    """Map page."""

    orientations = db.session.query(Orientation).all()
    genders = db.session.query(Gender).all()

    return render_template("map3.html", orientations=orientations, genders=genders)

@app.route("/map.json")
def map_json():
    """Map page."""

    #put this section into a function
    # make this a new object, return the object
    orientation = request.args.get("orientation")
    orientation = re.sub('orientation=','',orientation)
    orientation_list = re.split('&',orientation)
    gender = request.args.get("gender")
    gender = re.sub('gender=','',gender)
    gender = re.sub('\+',' ',gender)
    gender_list = re.split('&',gender)
    age = request.args.get("age")
    age_list = re.split(' \- ',age)

    locations = db.session.query(Location.location).all()


    compiled = {}
    i = 0
    for location in locations:

        location = location[0]
        #returns a list of tuples
        # cache and pre-fetch
        # asynchronous -- twisted

        # wrap into a function, get_joined_adjectives()
        print "location is", location
        adjective_list, population = get_joined_adjectives(orientation_list, gender_list, age_list, location)
        print "adjective list is", adjective_list

        latitude, longitude = get_lat_long(location)
        
        if adjective_list:

            adjective, count = calculate_word_count(adjective_list)
            
            compiled[location] = {}
            compiled[location] = add_adjective_to_compiled(compiled, location, latitude, longitude, population, adjective, count)
 

            i+=1
            if i % 10 == 0:
                print i, datetime.utcnow()

        else:
            compiled[location]= {}
            compiled[location] = add_nothing_to_compiled(compiled, location, latitude, longitude)
            
    return jsonify(compiled)


@app.route("/modal")
def modal():
    """Map page."""

    return render_template("modal.html")

if __name__ == "__main__":
    app.debug = True
    connect_to_db(app)

    # DebugToolbarExtension(app)
    app.run()