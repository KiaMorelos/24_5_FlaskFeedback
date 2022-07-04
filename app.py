"""Flask Feedback App"""
from flask import Flask, redirect, render_template, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Feedback
from forms import LoginUser, RegisterUser, FeedbackForm, DeleteFeedback

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
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def show_register_form():
    """Register a new user"""
    form = RegisterUser()
    if "username" in session:
        flash("You are already registered and logged in")
        return redirect(f"/users/{session['username']}")

    if form.validate_on_submit():
        data = {k: v for k, v in form.data.items() if k != "csrf_token"} 

        new_user = User.register(**data)
        db.session.add(new_user)
        db.session.commit()
        session["username"] = new_user.username
        return redirect(f'/users/{new_user.username}')
    else:
        return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def show_login_form():
    """Login User"""
    if "username" in session:
        flash("You are already logged in")
        return redirect(f"/users/{session['username']}")

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
    
    flash(f"Successfully logged out {session['username']}")
    session.pop("username")
    return redirect('/')

##User Routes##
@app.route('/users/<username>')
def show_user_details(username):
    """Show User Details Page"""

    if "username" not in session or username != session['username']:
        flash("You don't have the permissions to do that. Please login or choose a different action")
        return redirect('/')
    form = DeleteFeedback()
    user = User.query.get_or_404(username)
    return render_template('user-details.html', user=user, form=form)

@app.route('/users/<username>/delete', methods=['POST'])
def delete_user(username):
    """Delete User"""

    if "username" not in session or username != session['username']:
        flash("You don't have the permissions to do that. Please login or choose a different action")
        return redirect('/')
    
    user = User.query.get_or_404(username)
    session.pop("username")
    db.session.delete(user)
    db.session.commit()
    flash("Account Deleted")
    return redirect ('/')

## Feedback Routes
@app.route('/users/<username>/feedback/add', methods=['GET', 'POST'])
def add_feedback(username):
    """Show Add Feedback Form, add feedback to database"""

    if "username" not in session or username != session['username']:
        flash("You don't have the permissions to do that. Please login or choose a different action")
        return redirect('/')

    form = FeedbackForm()
    user = User.query.get_or_404(username)
    
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data      
       
        new_feedback = Feedback(title=title, content=content, username=username)
        db.session.add(new_feedback)
        db.session.commit()
        return redirect(f'/users/{username}')

    return render_template('new-feedback.html', form=form, user=user)

@app.route('/feedback/<int:feedback_id>/update', methods=['GET', 'POST'])
def update_feedback(feedback_id):
    """Show update form, update in db"""

    feedback = Feedback.query.get_or_404(feedback_id)
    user = feedback.username
    if "username" not in session or feedback.username != session['username']:
         flash("You don't have the permissions to do that. Please login or choose a different action")
         return redirect('/')

    form = FeedbackForm(obj=feedback)
    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data
        db.session.commit()
        return redirect(f'/users/{user}')

    return render_template('update-feedback.html', form=form, user=user)

@app.route('/feedback/<int:feedback_id>/delete', methods=['POST'])
def delete_feedback(feedback_id):
    """Delete feedback"""
    feedback = Feedback.query.get_or_404(feedback_id)
    user = feedback.username
    
    if "username" not in session or user != session['username']:
         flash("You don't have the permissions to do that. Please login or choose a different action")
         return redirect('/')

    form = DeleteFeedback()

    if form.validate_on_submit():
        db.session.delete(feedback)
        db.session.commit()

    return redirect(f'/users/{user}')