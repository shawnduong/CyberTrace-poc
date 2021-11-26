from app import *

from flask_login import current_user

@app.route("/"     , methods=["GET"])
@app.route("/login", methods=["GET"])
def index():
	"""
	Display the index page to the user.
	"""

	if current_user.is_authenticated:
		return render_template("stub.html")
	else:
		return render_template("index.html")

@app.route("/stub", methods=["GET"])
def stub():
	"""
	Stub for testing.
	"""

	print("DEBUG: STUB TRIGGERED.")
	return render_template("stub.html")

