#from distutils.command import check
from random import randrange
from flask import Blueprint, flash, render_template, request, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from .models import User
import traceback
import time

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        time.sleep(float(randrange(0, 100))/100)

        if (len(username) == 0):
            flash("Please enter a username.", category="error")
        elif (len(password) == 0):
            flash("Please enter a password.", category="error")
        else:
            user = db.session.query(User).filter_by(username=username).first()
            if user is not None:
                if check_password_hash(user.password, password):
                    flash("Logged in successfully!", category="success")
                    login_user(user, remember=True)
                    return redirect(url_for("views.dashboard"))
                else:
                    flash("Incorrect password, try again.", category="error")
            else:
                flash("Username does not exist.", category="error")
    time.sleep(0.1)
    return render_template("login.html", user=current_user)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        email = request.form.get("email")
        username = request.form.get("username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        print(email, username, password1, password2)

        user_email = db.session.query(User).filter_by(email=email).first()
        user_username = db.session.query(User).filter_by(username=username).first()
        if user_email is not None:
            flash("Email is taken.", category="error")
        elif user_username is not None:
            flash("Username is taken.", category="error")
        elif len(email) < 4:
            flash("Email must be greater than 3 characters.", category="error")
        elif len(username) < 2:
            flash("Username must be greater than 1 character.", category="error")
        elif password1 != password2:
            flash("Passwords don't match.", category="error")
        elif len(password1) < 7:
            flash("Password must be at least 7 characters.", category="error")
        else:
            #add user to the database
            new_user = User(email=email, password=generate_password_hash(password1, method="sha256"), username=username, litters_found=0, litters_cleaned=0, points=0, donationValue=0.0)
            print("New user:", new_user)
            
            db.session.add(new_user)
            db.session.commit() #updates the database
            flash("Account created!", category="success")
            login_user(new_user, remember=True)
            return redirect(url_for("views.dashboard")) #this doesn't redirect to a URL, it just redirects to the HTML file that should be rendered next.

    time.sleep(0.1)
    return render_template("signup.html", user=current_user)

from . import db