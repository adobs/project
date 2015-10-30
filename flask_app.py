from flask import Flask, request, render_template, redirect, flash, session
from jinja2 import StrictUndefined
from model import Profile, Adjective, db, connect_to_db
# from flask_debugtoolbar import DebugToolbarExtension
from selenium_okc import create_new_user
from sending_a_message import send_message
from signing_in import is_signed_in
import json 

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

    return results


@app.route("/new-user-landing", methods=["POST"])
def new_user_landing():
    """Is this page necessary"""
    
    flash("You have successfully created a new user")

    return redirect("/")

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

    print session
    
    return is_signed_in(screenname, password)

@app.route("/login-landing", methods=["POST"])
def login_landing():
    """Is this page necessary"""
    
    flash("You have successfully logged in")
    return redirect("/")


@app.route("/logout")
def logout():
    """Login page"""

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

    send_message(session["screenname"], session["password"], minimum_age, maximum_age, location, radius, gentation, message, num)

    flash("Message(s) successfully sent")

    return redirect("/")

@app.route("/map")
def map():
    """Map page."""

    adjectives = db.session.query(Adjective).all()
    profile_locations = db.session.query(Profile.location).all()
    json_compiled = {}
    for entry in adjectives:

        json_compiled[entry.location]= {}
        json_compiled[entry.location]['lat']=entry.latitude
        json_compiled[entry.location]['lng']=entry.longitude
        json_compiled[entry.location]['adj']=entry.adjective
        json_compiled[entry.location]['count']=entry.count
        json_compiled[entry.location]['population']= profile_locations.count(tuple([entry.location]))
    

    return render_template("map2.html", adjectives=json.dumps(json_compiled))

if __name__ == "__main__":
    app.debug = True
    connect_to_db(app)

    # DebugToolbarExtension(app)
    app.run()