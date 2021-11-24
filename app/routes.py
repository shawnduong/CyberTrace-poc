from app import app
from models import Users
from flask import render_template, request, redirect, url_for

# render the login page
@app.route("/", methods = ["GET"])
@app.route("/login", methods = ["GET"])
def index():
	return render_template("login.html")

@app.route("/register", methods = ["GET"])
def register():
	return redirect(url_for("login")) # placeholder for register page

# validate user login and direct them to either the app or a failed login screen
@app.route("/login", methods = ["POST"])
def login():
	username, password = request.form["username"], request.form["password"]
	print(username, password)

	if (user := Users.login(username, password)) == False:
		print("login failed")
		return redirect(url_for("register"))
	else:
		print("login worked")
		return redirect(url_for("login"))
