from flask import Flask, request, render_template, redirect
from jinja2 import StrictUndefined
from model import Profile, db, connect_to_db
# from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined

@app.route("/")
def home():
    """Home page; student and project lists (linked)."""
    generator = import_session.querying()
    print "here"
    import_session.searchOKC(generator)

    return "hi.  you are querying and inserting"

if __name__ == "__main__":
    app.debug=True
    connect_to_db(app)

    # DebugToolbarExtension(app)
    app.run()