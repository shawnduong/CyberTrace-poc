import time

from app import *

@app.route("/login", methods=["POST"])
def login():
	"""
	Authenticate the user, or return an error message if unsuccessful. For
	security, a brief delay is added before the user authentication is checked
	in order to slow down bruteforce/dictionary attacks.
	"""

	time.sleep(1)

	user = User.login(request.form["username"], request.form["password"])

	# Failed login condition.
	if user == False:
		return render_template("index.html", failed=True)

	# Successful login, account type admin.
	elif user.acctType == 0:
		# Stub.
		return render_template("index.html")

	# Successful login, account type non-admin.
	else:
		# Stub.
		return render_template("index.html")

