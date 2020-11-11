from flask import Blueprint, render_template, flash, redirect, url_for, request, session
from models.user import User
from werkzeug.security import check_password_hash
import re
from flask_login import login_required, current_user, login_user, logout_user


users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')


@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('users/new.html')


@users_blueprint.route("/", methods=['POST'])
def create():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    create_new_user = User(username = username, email = email, password = password)

    duplicate_username = User.get_or_none(User.username == username)
    duplicate_email = User.get_or_none(User.email == email)

    if create_new_user.save():
        return redirect("/")
    else:
        if duplicate_username: 
            flash("- This username has been used, please try another username")

        if duplicate_email:
            flash("- This email has been used, please try another email") 

        if len(password) < 6:
            flash("- Password must be at least 6 characters")

        if not re.search("[a-z]", password):
            flash("- Password must include lowercase and uppercase")
            
        if not re.search("[A-Z]", password):
            flash("- Password must include lowercase and uppercase")

        return redirect(url_for("users.new"))


@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
    user = User.get_or_none(User.username == username)
    return render_template("users/userprofile.html", user = user)


@users_blueprint.route('/login', methods=["GET"])
def login():
    return render_template("users/login.html")


@users_blueprint.route('/login/session', methods=[ 'POST' ])
def login_session():

    data = request.form
    user = User.get_or_none(username= data.get('username'))

    if user:
        hashed_password = user.password_hash # password hash stored in database for a specific user
        result = check_password_hash(hashed_password, data.get('password')) # what is result? Test it in Flask shell and implement it in your view function!

        if result:
           # session["user_id"] = user.id
            login_user(user)
            flash("Login successfully", 'success')
            return redirect(url_for('users.show',username = user.username))
        else:
            flash("Wrong password", 'error')
            return redirect(url_for('users.login'))
    else:
        flash("User not found", 'error')
        return redirect(url_for('users.login'))


@users_blueprint.route('/logout', methods=['POST'])
def logout():
    logout_user()
    flash('Signout Successfully', 'success')
    return redirect(url_for('users.login'))
