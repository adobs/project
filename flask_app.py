from flask import Flask, request, render_template, redirect, flash, session, jsonify
from jinja2 import StrictUndefined
from model import Profile, Adjective, Gender, Orientation, UsernameGender, Location, db, connect_to_db
# from flask_debugtoolbar import DebugToolbarExtension
from selenium_okc import create_new_user
from sending_a_message import send_message
from signing_in import is_signed_in
import re
# from calculate_word_count import calculate_word_count
# from datetime import datetime
# from map_helper import get_joined_adjectives, get_lat_long, add_adjective_to_compiled, add_nothing_to_compiled
from map_helper import get_compiled
from send_message_map import send
from create_json_for_d3_hierarchical import create_json
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


    result = send_message(session["screenname"], session["password"], minimum_age, maximum_age, location, radius, gentation, message, num)
    
    if result:
        return result
    else: 
        flash("Message(s) successfully sent")
        return ""

@app.route("/map")
def map():
    """Map page."""

    orientations = db.session.query(Orientation).order_by(Orientation.orientation).all()
    genders = db.session.query(Gender).order_by(Gender.gender).all()

    return render_template("map3.html", orientations=orientations, genders=genders)


@app.route("/map-checked.json")
def map_checked_json():
    """Map page."""

    #put this section into a function
    # make this a new object, return the object
    orientation = request.args.get("orientation")
    orientation = re.sub('orientation=','',orientation)
    orientation_list = re.split('&',orientation)
    orientation_tuple=tuple(orientation_list)
    gender = request.args.get("gender")
    gender = re.sub('gender=','',gender)
    gender = re.sub('\+',' ',gender)
    gender_list = re.split('&',gender)
    gender_tuple = tuple(gender_list)
    age = request.args.get("age")
    age_list = re.split(' \- ',age)

    age_min, age_max = age_list

    logged_in = "False"
    # if logged in
    if session.get("screenname"):
        logged_in = "True"


    # users = db.session.query(Profile.username).filter(
    #     Profile.orientation.in_(orientation_tuple)).filter(
    #     Profile.gender.in_(gender_tuple)).filter(
    #     Profile.age >= age_min).filter(Profile.age <= age_max)


    # results = db.session.query(Adjective.username, Profile.location, 
    #                            Adjective.adjective, Location.latitude, 
    #                            Location.longitude).join(Profile).join(
    #                            Location).filter(Adjective.username.in_(users)).all()

    QUERY = """SELECT A.Username, P.location, A.adjective, L.latitude, L.longitude 
               FROM Adjectives AS A JOIN Profiles AS P ON P.username=A.username 
               JOIN Locations AS L on P.Location = L.Location 
               WHERE A.Username IN ( 
                SELECT Username FROM Profiles 
                WHERE Age BETWEEN :age_min 
                AND :age_max AND Username 
                IN (
                    SELECT Username FROM Usernameorientations 
                    WHERE Orientation IN :orientation_tuple 
                    AND Username IN (
                        SELECT Username FROM Usernamegenders 
                        WHERE Gender IN :gender_tuple)))
            """

    cursor = db.session.execute(QUERY, {"age_min": age_min, 
                    "age_max": age_max, "orientation_tuple": orientation_tuple, "gender_tuple": gender_tuple})
    
    results = cursor.fetchall()

    print "results is,", results
    
    compiled = get_compiled(logged_in, results)
    print "end of json"
    return jsonify(compiled)



@app.route("/send-message.json", methods=["POST"])
def send_messages_map():
    """Send message to OKCupid users."""

    recipients = request.form.get("recipients")
    recipient_list = recipients.split(", ")
    message = request.form.get("message")

    username = session["screenname"]
    password = session["password"]

    send(username, password, recipient_list, message)

    return "hello"


@app.route("/d3page")
def d3_page():


    return render_template("hierarchical_edge_building.html")


@app.route("/sendjson")
def send_json():

    graph = json.dumps(create_json("quirky"))

    print "json is", graph

    return graph



if __name__ == "__main__":
    app.debug = True
    connect_to_db(app)

    # DebugToolbarExtension(app)
    app.run()