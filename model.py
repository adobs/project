from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
# This is the connection to the SQLite database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Model definitions

class Profile(db.Model):
    """Profile information."""

    __tablename__ = "profiles"

    username = db.Column(db.Text, primary_key=True, )
    timestamp = db.Column(db.DateTime, nullable=False, default = datetime.utcnow)
    age = db.Column(db.Integer, nullable=True)
    location = db.Column(db.Text, nullable=True)
    gender = db.Column(db.Text, nullable=True)
    orientation = db.Column(db.Text, nullable=True)
    self_summary = db.Column(db.Text, nullable=True)
    my_life = db.Column(db.Text, nullable=True)
    good_at = db.Column(db.Text, nullable=True)
    people_first_notice = db.Column(db.Text, nullable=True)
    favorites = db.Column(db.Text, nullable=True)
    six_things = db.Column(db.Text, nullable=True)
    think_about = db.Column(db.Text, nullable=True)
    friday_night = db.Column(db.Text, nullable=True)
    private_admission = db.Column(db.Text, nullable=True)
    message_me_if = db.Column(db.Text, nullable=True)



class Adjective(db.Model):
    """Profile information."""

    __tablename__ = "adjectives"

    location = db.Column(db.Text, primary_key=True)
    adjective = db.Column(db.Text, nullable=True)
    count = db.Column(db.Integer, nullable=True)



def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our SQLite database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///profiles_10_25_4.db'
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.
    from flask_app import app

    connect_to_db(app)
    print "Connected to DB."
