#!/usr/bin/env python3

# Test to see if the middleware POSTs information as intended.

from flask import *

# Instantiate the application.
app = Flask(__name__)

@app.route("/api/report", methods=["POST"])
def report():
	"""
	Receive some POSTed JSON data about an attack.
	"""

	print(request.json)

	return {"STATUS": "RECEIVED"}, 200

if __name__ == "__main__":
	app.run(host="127.0.0.1", port=8080)
