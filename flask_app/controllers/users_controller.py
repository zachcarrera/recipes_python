from flask import render_template, redirect, request, session

from flask_app import app
from flask_app.models.users_model import User



# route to main login page
@app.route("/")
def index():
    return render_template("index.html")


# form submission for registering
@app.route("/register", methods=["POST"])
def register():

    if not User.validate_new(request.form):
        return redirect("/")
    
    session["user_id"] = User.create(request.form)
    return redirect("/recipes")



# form submission for logging in
@app.route("/login", methods=["POST"])
def login():
    logged_in_user =  User.validate_login(request.form)

    if not logged_in_user:
        return redirect("/")

    session["user_id"] = logged_in_user.id
    return redirect("/recipes")


# route to log out user
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")