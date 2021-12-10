from app import *
from sqlalchemy import *

@app.route("/api/report", methods=["POST"])
def report():
	"""
	Receive some POSTed JSON data about an event and store it in the event
	table in the database.
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
		)
		db.session.add(event)
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
			}

		return response, 200

	except:
		return "Unexpected error.", 500

