"""Flask Feedback App"""
from flask import Flask, redirect, render_template, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User
from forms import LoginUser, RegisterUser

app = Flask(__name__)
app.config['SECRET_KEY'] = "its_a_secret_to_everybody"
debug = DebugToolbarExtension(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///flask_feedback_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

@app.route('/')
def root_route():
    return redirect('/register')

@app.route('/register', methods=['GET', 'POST'])
def show_register_form():
    """Register a new user"""
    form = RegisterUser()

    if form.validate_on_submit():
        data = {k: v for k, v in form.data.items() if k != "csrf_token"} 

        new_user = User.register(**data)
        db.session.add(new_user)
        db.session.commit()
        session["username"] = new_user.username
        return redirect(f'/users/{new_user.username}')
    else:
        return render_template('register.html', form=form)

@app.route('/users/<username>')
def show_secret(username):
    """Show Secret Content"""

    if "username" not in session or username != session['username']:
        flash("You don't have the permissions to do that. Please login or choose a different action")
        return redirect('/login')
    else:
        user = User.query.get_or_404(username)
        return render_template('user-details.html', user=user)

@app.route('/login', methods=['GET', 'POST'])
def show_login_form():
    """Login User"""
    
    form = LoginUser()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.authenticate(username, password)

        if user:
            session["username"] = user.username
            return redirect(f'/users/{user.username}')
        else:
            form.username.errors = ["Bad username/password"]

    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    """Log out and redirect to homepage"""

    session.pop("username")
    flash("Successfully logged out!")
    return redirect('/')