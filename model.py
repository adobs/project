from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime
from sqlalchemy.dialects import postgresql
# This is the connection to the SQLite database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Model definitions

class Profile(db.Model):
    """Profile information."""

    __tablename__ = "profiles"

    username = db.Column(db.Text, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False, default = datetime.utcnow)
    age = db.Column(db.Integer, nullable=True)
    location = db.Column(db.Text, db.ForeignKey('locations.location'), nullable=True)
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

class MeanShiftAlgo(db.Model):
    """Mean shift algortithm resulting labels for user"""

    __tablename__ = "meanshiftalgos"

    username = db.Column(db.Text, db.ForeignKey('profiles.username'), primary_key=True)
    self_summary_label = db.Column(db.Integer, nullable=True)
    message_me_if_label = db.Column(db.Integer, nullable=True)

    profile = db.relationship('Profile', backref=db.backref('meanshiftalgos'))

class OldAdjective(db.Model):
    """List of adjectives per user"""

    __tablename__ = "oldadjectives"

    username = db.Column(db.Text, db.ForeignKey('profiles.username'), primary_key=True)
    adjectives = db.Column(postgresql.ARRAY(db.Text), nullable=False)

    profile = db.relationship('Profile', backref=db.backref('oldadjectives'))



class Adjective(db.Model):
    """List of adjectives per user"""

    __tablename__ = "adjectives"

    adjective_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.Text, db.ForeignKey('profiles.username'), nullable=False)
    adjective = db.Column(db.Text)

    profile = db.relationship('Profile', backref=db.backref('adjectives'))


class Orientation(db.Model):
    """List of orientations in database"""

    __tablename__ = "orientations"

    orientation = db.Column(db.Text, primary_key=True)


    profiles = db.relationship("Profile", secondary="usernameorientations", lazy="dynamic", backref=db.backref("orientations", lazy="dynamic"))

class UsernameOrientation(db.Model):
    """User matched up with their orientation"""

    __tablename__ = "usernameorientations"

    username_orientation_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.Text, db.ForeignKey("profiles.username"), nullable=False)
    orientation = db.Column(db.Text, db.ForeignKey("orientations.orientation"), nullable=False)

    # orientations = db.relationship('Orientation', backref=db.backref("usernameorientations", lazy='dynamic'))
    # profile = db.relationship('Profile', backref=db.backref("usernameorientations",lazy='dynamic'))


class Gender(db.Model):
    """List of genders in database"""

    __tablename__ = "genders"

    gender = db.Column(db.Text, primary_key=True)

    profiles = db.relationship("Profile", secondary="usernamegenders", lazy="dynamic", backref=db.backref("genders", lazy="dynamic"))


class UsernameGender(db.Model):
    """User matched up with their gender"""

    __tablename__ = "usernamegenders"

    username_gender_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.Text, db.ForeignKey('profiles.username'), nullable=False)
    gender = db.Column(db.Text, db.ForeignKey('genders.gender'), nullable=False)

    # genders = db.relationship('Gender', backref=db.backref('usernamegenders', lazy='dynamic'))
    # profile = db.relationship('Profile', backref=db.backref('usernamegenders', lazy='dynamic'))


class Location(db.Model):
    """List of locations and lat/long"""

    __tablename__ = "locations"

    location = db.Column(db.Text, primary_key=True)
    latitude = db.Column(db.Numeric)
    longitude = db.Column(db.Numeric)

    profile = db.relationship('Profile', backref=db.backref('locations'))


class Zipcode(db.Model):
    """List of zipcodes."""

    __tablename__ = "zipcodes"

    zipcodes = db.Column(db.Text, primary_key=True)



def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our SQLite database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///profiles'
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.
    from flask_app import app

    connect_to_db(app)
    print "Connected to DB."
    db.create_all()
