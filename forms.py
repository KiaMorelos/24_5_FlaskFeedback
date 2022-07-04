from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField
from wtforms.validators import InputRequired

class RegisterUser(FlaskForm):
    """Form to register a user"""

    username = StringField("Username", validators=[InputRequired(message="Please enter a username")])

    password = PasswordField("Password", validators=[InputRequired(message="Please enter a password")])

    email = EmailField("Email Address", validators=[InputRequired(message="Please enter an email")])

    first_name = StringField("First Name", validators=[InputRequired(message="Please enter your first name")])

    last_name = StringField("Last Name", validators=[InputRequired(message="Please enter your last name")])
            

class LoginUser(FlaskForm):
    """Login User"""
    username = StringField("Username", validators=[InputRequired(message="Please enter a username")])
    password = PasswordField("Password", validators=[InputRequired(message="Please enter a password")])