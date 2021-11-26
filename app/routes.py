from app import *

from flask_login import current_user, login_required

@app.route("/"     , methods=["GET"])
@app.route("/login", methods=["GET"])
def index():
	"""
	Display the index page to the user.
	"""

	if current_user.is_authenticated:
		return redirect(url_for("application"))
	else:
		return render_template("index.html")

@app.route("/app", methods=["GET"])
@login_required
def application():
	"""
	Display the application to the user. This isn't named "app" to avoid a
	namespace collision with the Flask "app."
	"""

	return render_template("vectormap.html")

@app.route("/stub", methods=["GET"])
@login_required
def stub():
	"""
	Stub for testing.
	"""

	print("DEBUG: STUB TRIGGERED.")
	return render_template("stub.html")

