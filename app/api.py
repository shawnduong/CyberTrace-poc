from app import *

@app.route("/api/report", methods=["POST"])
def report():
	"""
	Receive some POSTed JSON data about an attack.
	"""

	print(request.json)

	return {"STATUS": "RECEIVED"}, 200

