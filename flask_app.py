from flask import Flask, request, render_template, redirect, flash, session, jsonify, g
from jinja2 import StrictUndefined
from model import Profile, Adjective, Gender, Orientation, Location, db, connect_to_db
# from flask_debugtoolbar import DebugToolbarExtension
from selenium_okc import create_new_user
from sending_a_message import send_message
from signing_in import is_signed_in
import re
from okcupyd.session import Session
from okcupyd.user import User
# from calculate_word_count import calculate_word_count
# from datetime import datetime
# from map_helper import get_joined_adjectives, get_lat_long, add_adjective_to_compiled, add_nothing_to_compiled
from map_helper import get_compiled
from send_message_map import send
# from create_json_for_d3_hierarchical import create_json
from markov import get_input_text, make_chains, make_text
import json

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined

JS_TESTING_MODE = False

@app.before_request
def add_tests():
    g.jasmine_tests = JS_TESTING_MODE

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

    locations = db.session.query(Location).all()

    return render_template("okcbot.html", locations=locations)




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


    users = db.session.query(Profile.username).filter(
        Profile.orientation.in_(orientation_tuple)).filter(
        Profile.gender.in_(gender_tuple)).filter(
        Profile.age >= age_min).filter(Profile.age <= age_max)


    results = db.session.query(Adjective.username, Profile.location, 
                               Adjective.adjective, Location.latitude, 
                               Location.longitude).join(Profile).join(
                               Location).filter(Adjective.username.in_(users)).all()

    # QUERY = """SELECT A.Username, P.location, A.adjective
    #            FROM Adjectives AS A JOIN Profiles AS P ON P.username=A.username 
    #            WHERE A.Username IN ( 
    #             SELECT Username FROM Profiles 
    #             WHERE Age BETWEEN :age_min 
    #             AND :age_max AND Username 
    #             IN (
    #                 SELECT Username FROM Usernameorientations 
    #                 WHERE Orientation IN :orientation_tuple 
    #                 AND Username IN (
    #                     SELECT Username FROM Usernamegenders 
    #                     WHERE Gender IN :gender_tuple)))
    #         """

    # cursor = db.session.execute(QUERY, {"age_min": age_min, 
    #                 "age_max": age_max, "orientation_tuple": orientation_tuple, "gender_tuple": gender_tuple})
    
    # results = cursor.fetchall()

    # print "results is,", results
    
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

@app.route("/markov")
def markov():

    orientations = db.session.query(Orientation).order_by(Orientation.orientation).all()
    genders = db.session.query(Gender).order_by(Gender.gender).all()
    locations = db.session.query(Location).all()
    adjectives = db.session.query(Adjective).distinct(Adjective.adjective).order_by(Adjective.adjective).all()
    
    def adjectiveg(adjectives):
        for adjective in adjectives:
            yield adjective.adjective.strip("\"#$%&'()*+-/:;<=>@[\\]^_`{|}~1234567890")

    adjective_generator = adjectiveg(adjectives)

    return render_template("markov.html", orientations=orientations, genders=genders, locations=locations, adjective_generator=adjective_generator)


@app.route("/markov.json")
def markov_json():
    
    orientation = request.args.get("orientation")
    gender = request.args.get("gender")
    age = request.args.get("age")
    age_list = re.split(' \- ',age)
    age_min, age_max = age_list
    location = request.args.get("location")
    # radius = request.args.get("radius")
    n = int(request.args.get("randomness"))
    adjective1 = request.args.get("adjective1")
    adjective2 = request.args.get("adjective2")
    adjective3 = request.args.get("adjective3")
    # adjective4 = request.args.get("adjective4")
    # adjective5 = request.args.get("adjective5")

    adjective_list = [adjective1, adjective2, adjective3]

    # location_list = get_list_of_locations(location, radius)
    
    text_string = get_input_text(orientation, gender, location, age_min, age_max, adjective_list, n)
    
    if text_string == "invalid search results":
        return text_string
    else:
        chains = make_chains(text_string, n)
        text = make_text(chains)

        return text

@app.route("/markov-adjectives.json")
def markov_adjective_json():
    orientation = request.args.get("orientation")
    gender = request.args.get("gender")
    age = request.args.get("age")
    age_list = re.split(' \- ',age)
    age_min, age_max = age_list
    location = request.args.get("location")

    adjectives = db.session.query(Adjective.adjective.distinct()).join(Profile).filter(Profile.orientation.like(
                    "%"+orientation+"%")).filter(Profile.location==location).filter(Profile.gender.like("%"+gender+"%")).filter(
                    Profile.age>=age_min).filter(Profile.age<=age_max).order_by(Adjective.adjective).all()

    adjective_list = [adjective[0] for adjective in adjectives]
    return json.dumps(adjective_list)

@app.route("/add-to-profile.json", methods=["POST"])
def add_to_profile_json():

    text = request.form.get("text")

    screenname = session["screenname"]
    password = session["password"]
    session_ = Session.login(screenname, password)
    user = User(session=session_)
    user.profile.essays.self_summary = text

    return "success"

if __name__ == "__main__":
    app.debug = True
    connect_to_db(app)

    # DebugToolbarExtension(app)
    app.run() 
    import sys
    if sys.argv[-1] == "jstest":
        JS_TESTING_MODE = True