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
from send_message_map import send_message_map

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


@app.route("/map-markers.json")
def map_markers_json():
    """Map page."""

    print "pre query"

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


    QUERY = """SELECT Profiles.username, Profiles.location, Adjectives.adjective, Locations.latitude, Locations.longitude  
                FROM Profiles JOIN Adjectives ON Profiles.username=Adjectives.username 
                JOIN Locations ON Profiles.location=Locations.location
                WHERE Profiles.username IN
                    (SELECT P.username FROM Profiles AS P 
                    JOIN Usernameorientations AS UO on P.username = UO.username 
                    JOIN Usernamegenders AS UG on UO.username = UG.username 
                    WHERE UO.Orientation in :orientation_list 
                    AND UG.Gender in :gender_list 
                    AND P.Age BETWEEN :age_min AND :age_max)"""

    cursor = db.session.execute(QUERY, {'orientation_list': orientation_tuple, 'gender_list': gender_tuple, 'age_min': age_min, 'age_max': age_max})

    results = cursor.fetchall()

    compiled = {}

    word_count = {}

    print results
    for result in results:
        username, location, adjective, latitude, longitude = result

        # get list of words by location
        word_count[location] = word_count.get(location,{})
        word_count[location]["word"] = word_count[location].get("word",[])
        word_count[location]["profile_list"] = word_count[location].get("profile_list",[])
        word_count[location]["word"].append(adjective)
        word_count[location]["profile_list"].append(username)


        compiled[location] = compiled.get(location, {})
        compiled[location]['lat'] = float(latitude)
        compiled[location]['lng'] = float(longitude)
        compiled[location]['location'] = location


    
    for location in word_count:
        unique_profiles = list(set(word_count[location]["profile_list"]))
        population = len(unique_profiles)
        word_list = word_count[location]["word"]
        most_common_adjective, most_common_count = calculate_word_count(word_list)        

        profile_index =[]

        for i, word in enumerate(word_count[location]["word"]):
            if word == most_common_adjective:
                profile_index.append(i)

                # print "word is ", word
                # print "i is", i
                # print "lenth is", len(word_count[location]["profile_list"])

        profiles = []
        for item in profile_index:
            profiles.append(word_count[location]["profile_list"][item])

        profiles = list(set(profiles))

        compiled[location]['adj'] = most_common_adjective
        compiled[location]['count'] = most_common_count
        compiled[location]['profile_list'] = unique_profiles
        compiled[location]['profiles']=profiles
        compiled[location]['population'] = population

    print "\n!!!! length of word count", len(word_count)
    return jsonify(compiled)


@app.route("/map-html.json", methods=["POST"])
def map_html_json():
    """Map page."""
    html = request.form.get("html")

    # <div hidden>Cmurph111,LizStormborn,AliceRose516,ArtsyDelight</div><div hidden>LizStormborn,Cmurph111,chibichaan,AliceRose516,smartsweesinger,ArtsyDelight,sunmusic89,b3liz3an_qu33n,jeeLi</div><

    print "html is", html
    
    if "hidden" in html:
        short_list, long_list = re.findall(r'<div hidden>(.*?)</div>', html)
        
        print "short list is", short_list
        print "long list is", long_list
        short_list = short_list.split(",")
        short_list = (", ").join(short_list)
        long_list = long_list.split(",")
        long_list = (", ").join(long_list)
        profiles = {"short_list": short_list, "long_list": long_list}

        return jsonify(profiles)

    return ""

@app.route("/send-message.json", methods=["POST"])
def send_messages_map():
    """Send message."""
    
    # check to see that user is logged in
    # check that I am getting correct inputs
        
    recipients = request.form.get("recipients")
    recipient_list = recipients.split(",")
    message = request.form.get("message")
    print "recipients", recipients
    print "recipient_list", recipient_list
    print "message is", message

    username = session["screenname"]
    password = session["password"]
    print "username is", username

    send_message_map(username, password, recipient_list, message)

    return "hello"

@app.route("/d3page")
def d3_page():

    return render_template("force_layout_advanced.html")

if __name__ == "__main__":
    app.debug = True
    connect_to_db(app)

    # DebugToolbarExtension(app)
    app.run()