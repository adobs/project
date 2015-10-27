from flask import Flask, request, render_template, redirect
from jinja2 import StrictUndefined
from model import Profile, db, connect_to_db
# from flask_debugtoolbar import DebugToolbarExtension
from okcupyd.session import Session
from okcupyd.json_search import SearchFetchable
from selenium_okc import create_new_user

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined

@app.route("/")
def home():
    """Home page; student and project lists (linked)."""


    return "hi"

@app.route("/new-user-form")
def new_user_form():
    """Registration form"""

    # username



    return render_template("create_new_user_form.html")


@app.route("/new-user", methods="POST")
def create_a_new_user():
    """Home page; student and project lists (linked)."""
    
    orientation = request.form.get("orientation")
    gender = request.form.get("gender")
    birthmonth = request.form.get("birthmonth")
    birthdate = request.form.get("birthdate")
    birthyear = request.form.get("birthyear")
    zip = request.form.get("zip")
    email = request.form.get("email")
    screenname = request.form.get("screenname")
    password = request.form.get("password")

    print "hello"
    print orientation 
    print gender 
    print birthmonth 
    print birthdate 
    print birthyear
    print zip 
    print email 
    print screenname 
    print password 


    return create_new_user(orientation, gender, birthmonth, birthdate, birthyear, zip, email, screenname, password)

@app.route("/new-user-landing", methods="POST")
def new_user_landing():
    """Home page; student and project lists (linked)."""
 
    return redirect("/")

if __name__ == "__main__":
    app.debug=True
    connect_to_db(app)

    # DebugToolbarExtension(app)
    app.run()