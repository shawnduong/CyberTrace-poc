import hashlib

from app import *
from sqlalchemy import *

@app.route("/api/list", methods=["GET"])
@login_required
def hlist():
	"""
	Give the user a JSON list of hosts they are associated with. This function
	is called hlist to prevent a collision with the Python list function.
	"""

	try:
		hosts = []

		for result in Association.query.filter_by(user=current_user.id).all():
			host  = result.id
			hosts.append(Host.query.get(host).ip)

		return {"HOSTS": hosts}

	except:
		return {"STATUS": "ERROR"}, 500

@app.route("/api/add", methods=["POST"])
@login_required
def add():
	"""
	Verify that the user has the correct host key for the IP address, and then
	associate them if their association does not already exist.
	"""

	try:

		ip  = request.form["host_ip"]
		key = request.form["host_key"]

		# Check if the host exists in the database.
		if not (q:=Host.query.filter_by(ip=ip).first()):
			return {"STATUS": "UNAUTHORIZED"}, 200

		# Check if the association already exists.
		if Association.query.filter_by(user=current_user.id, host=q.id).first():
			return {"STATUS": "PRE-EXISTENT"}, 200

		# Check if the host key is correct.
		if not (k:=hashlib.sha1((key+ip).encode()).hexdigest()) == q.key:
			return {"STATUS": "UNAUTHORIZED"}, 200

		# Add the association.
		association = Association(current_user.id, q.id)
		db.session.add(association)
		db.session.commit()

		# Send feedback.
		return {"STATUS": "SUCCESSFUL"}, 200

	except:
		return {"STATUS": "ERROR"}, 500

@app.route("/api/report", methods=["POST"])
def report():
	"""
	Receive some POSTed JSON data about an event and store it in the event
	table in the database. Additionally, store the host key in the database
	if it is not already present.
	"""

	try:
		event = Event(
			request.json["epoch_timestamp"],
			request.json["module_id"],
			request.json["module_name"],
			request.json["module_description"],
			request.json["attack_type"],
			request.json["attack_description"],
			request.json["victim_ip_version"],
			request.json["victim_ip_address"],
			request.json["victim_lat"],
			request.json["victim_lon"],
			request.json["attacker_ip_version"],
			request.json["attacker_ip_address"],
			request.json["attacker_lat"],
			request.json["attacker_lon"],
			request.json["traceroute"],
		)
		db.session.add(event)
		db.session.commit()

		if not Host.query.filter_by(ip=request.json["victim_ip_address"]).first():
			host = Host(
				request.json["victim_ip_address"],
				request.json["host_key"]
			)
			db.session.add(host)
			db.session.commit()

		return {"STATUS": "RECEIVED"}, 200

	except:
		return {"STATUS": "ERROR"}, 500

@app.route("/api/update/<since>", methods=["GET"])
@login_required
def update(since):
	"""
	Return all events after a given event serial number "since." If the "since"
	is -1, then that means that the client just initialized and does not know
	where the database is currently at. In that case, return the max ID.
	"""

	try:
		since = int(since)

		# -1 implies app just initialized and therefore needs to first define
		# the head before continuing.
		if since == -1:
			return {"HEAD": db.session.query(func.max(Event.id)).scalar()}, 200

		response = {}

		for event in db.session.query(Event).filter(Event.id > since).all():

			# If the user is not associated with the host associated with this
			# event, then skip over this event.
			if not (hostID:=Host.query.filter_by(ip=event.victim_ip_address).first()):
				continue
			if not Association.query.filter_by(user=current_user.id, host=hostID.id).first():
				continue

			response[event.id] = {
				"epoch_timestamp"      : event.epoch_timestamp,
				"module_id"            : event.module_id,
				"module_name"          : event.module_name,
				"module_description"   : event.module_description,
				"attack_type"          : event.attack_type,
				"attack_description"   : event.attack_description,
				"victim_ip_version"    : event.victim_ip_version,
				"victim_ip_address"    : event.victim_ip_address,
				"victim_lat"           : event.victim_lat,
				"victim_lon"           : event.victim_lon,
				"attacker_ip_version"  : event.attacker_ip_version,
				"attacker_ip_address"  : event.attacker_ip_address,
				"attacker_lat"         : event.attacker_lat,
				"attacker_lon"         : event.attacker_lon,
				"traceroute"           : event.traceroute,
			}

		return response, 200

	except:
		return "Unexpected error.", 500

