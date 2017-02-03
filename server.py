"""Movie Ratings."""

from flask import Flask, render_template, redirect, request, flash, session, jsonify

from model import User, Rating, Movie, connect_to_db, db

from jinja2 import StrictUndefined

from flask_debugtoolbar import DebugToolbarExtension


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""
    
    return render_template("homepage.html")

@app.route('/register', methods=["GET"])
def register_form():
    """Show sign-up form."""

    return render_template("register_form.html")

@app.route('/register', methods=["POST"])
def register_process():
    """Show sign-up form."""

    email = request.form.get('email')
    password = request.form.get('password')

    # user = User('whatever@gmail.com', '')
    # user = User.query.filter_by(email=email).one()
    new_user = User(email=email, password=password)
    # if user != email:
    # # username and password in session
    #     flash("You're already registered!")
    #     return redirect("/")
    # else:
    #     QUERY = """
    #     INSERT INTO User 
    #     VALUES (:email, :password)
    #     """
        
    db.session.add(new_user)
    db.session.commit()

    flash("User %s added." % email)
    return redirect("/")
    

@app.route('/login', methods=["GET"])
def login_form():
    """Show sign-in form"""

    return render_template("login_form.html")


@app.route('/login', methods=["POST"])
def login_process():
    """Process sign-in form."""

    email = request.form['email']
    password = request.form['password']

    user = User.query.filter_by(email=email).first()

    if not user:
        # session['username'] = email
        flash("You don't exist")
        return redirect("/login")
    
    if user.password != password:
        flash("Wrong password!")
        return redirect("/login")

    session["user_id"] = user.user_id

    flash("You're logged in!")
    return redirect("/users/%s" % user.user_id)


@app.route("/users")
def user_list():
    """Show list of users."""

    users = User.query.all()
    return render_template("user_list.html", users=users)




if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)


    
    app.run(port=5000, host='0.0.0.0')
