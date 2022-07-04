"""Models for Flask Feedback"""

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()

class User(db.Model):
    """Users Model"""

    __tablename__ = "users"

    username = db.Column(db.String(20), primary_key=True, unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)

    feedback = db.relationship("Feedback", backref="user", cascade="all,delete")

    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        """Register new user return hashed password"""
        hashed_pass = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed_pass.decode("utf8")

        return cls(username=username, password=hashed_utf8, email=email, first_name=first_name, last_name=last_name)

    @classmethod
    def authenticate(cls, username, pw):
        """Authenticate user"""
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, pw):
            return user
        else: 
            return False

class Feedback(db.Model):
    """Feedback Model"""
    
    __tablename__ = "feedback"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    username = db.Column(db.String, db.ForeignKey('users.username'), nullable=False)

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)