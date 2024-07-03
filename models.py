from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime

db = SQLAlchemy()

bcrypt = Bcrypt()

def connect_db(app):
    """Connect to the db."""
    db.app = app
    db.init_app(app)

class User(db.Model):
    """User Model"""

    __tablename__ = 'users'

    username = db.Column(db.String(20), primary_key=True, nullable=False,  unique=True)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)

    @classmethod
    def register(cls, username, pwd, email):
        """Register user w/hashed password & return user."""

        hashed = bcrypt.generate_password_hash(pwd)
        # turn bytestring into normal (unicode utf8) string
        hashed_utf8 = hashed.decode("utf8")

        # return instance of user w/username and hashed pwd
        return cls(username=username, password=hashed_utf8, email=email)

    @classmethod
    def authenticate(cls, username, pwd):
        """Validate that user exists & password is correct.

        Return user if valid; else return False.
        """
        
        u = User.query.filter_by(username=username).first()

        if u and bcrypt.check_password_hash(u.password, pwd):
            # return user instance
            return u
        else:
            return False
        
class Exercise(db.Model):
    """Exercise Model"""

    __tablename__ = 'exercises'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)

class UserExercise(db.Model):
    """Model to link the users and exercises databases"""

    __tablename__ = 'user_exercises'

    user = db.Column(db.String(20), db.ForeignKey('users.username'), nullable=False, primary_key=True)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False, primary_key=True)

    user_rel = db.relationship("User", backref="user_exercises")
    exercise_rel = db.relationship("Exercise", backref="user_exercises")

class WorkoutEntry(db.Model):
    """Workout Entry Model"""

    __tablename__ = 'workout_entries'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user = db.Column(db.String(20), db.ForeignKey('users.username'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    description = db.Column(db.Text, nullable=True)

    user_rel = db.relationship("User", backref="workout_entries")