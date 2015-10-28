from flask import Flask, request, render_template, redirect, flash, session
from jinja2 import StrictUndefined
from model import Profile, Adjective, db, connect_to_db
# from flask_debugtoolbar import DebugToolbarExtension
from okcupyd.session import Session
from okcupyd.json_search import SearchFetchable
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


    return render_template("create_new_user_form.html")


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

    session["screenname"] = screenname
    session["password"] = password

    return create_new_user(orientation, gender, birthmonth, birthdate, birthyear, zipcode, email, screenname, password)

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

    if is_signed_in(screenname, password):
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
    gentation = request.form.get("gentation")
    word = request.form.get("word")
    message = request.form.get("message")
    num = int(request.form.get("num"))

    print session["screenname"]
    print session["password"]

    send_message(session["screenname"], session["password"], minimum_age, maximum_age, gentation, message, num, word)

    flash("Message(s) successfully sent")

    return redirect("/")

@app.route("/map")
def map():
    """Map page.  VERY BROKEN"""

    adjective = db.session.query(Adjective)
    cols = Adjective.__table__.columns
    json_compiled = {}
    for entry in adjective:
        json_compiled[adjective.location]['lat']=adjective.latitude
        json_compiled[adjective.location]['lng']=adjective.longitude
        json_compiled[adjective.location]['adj']=adjective.adjective
        json_compiled[adjective.location]['count']=adjective.count
     
    return render_template("map.html", adjectives=json.dumps({"lat": 180, "lng": 240}))

if __name__ == "__main__":
    app.debug = True
    connect_to_db(app)

    # DebugToolbarExtension(app)
    app.run()