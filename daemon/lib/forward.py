import ipaddress
import requests
import socket
import time

from lib.auxiliary import *
from lib.ModuleDB import *
from termcolor import colored

def forward(db: ModuleDB, sock: socket.socket, ip: str, port: int, api: str) -> None:
	"""
	Receive some data from the socket and forward it to the given API endpoint
	ip:port/api in the form of JSON data.
	"""

	# Receive data through the socket.
	data = sock.recv(2048)

	# Process the data.
	while len(data) > 0:

		# Template for JSON data to POST.
		json = {
			# Time information.
			"epoch_timestamp"      : None,

			# Module information.
			"module_id"            : None,
			"module_name"          : None,
			"module_version"       : None,
			"module_description"   : None,

			# Attack information.
			"attack_type"          : None,
			"attack_description"   : None,

			# Victim information.
			"victim_ip_version"    : None,
			"victim_ip_address"    : None,
			"victim_lat"           : None,
			"victim_lon"           : None,

			# Attacker information.
			"attacker_ip_version"  : None,
			"attacker_ip_address"  : None,
			"attacker_lat"         : None,
			"attacker_lon"         : None,
		}

		# Time information.
		json["epoch_timestamp"] = int(time.time())

		# Module ID.
		json["module_id"] = int.from_bytes(data[:4], "big")
		module = db.session.query(db.Module).get(json["module_id"])

		# Module information.
		json["module_name"]         = module.name
		json["module_version"]      = module.version
		json["module_description"]  = module.description

		# Attack ID.
		json["attack_type"] = int.from_bytes(data[4:8], "big")
		attack = db.session.query(db.Attack).filter_by(
			moduleID=json["module_id"], attackID=json["attack_type"]).first()

		# Attack information.
		json["attack_description"] = attack.description

		# Attacker IP version.
		json["attacker_ip_version"] = int(data[8])

		# Attacker IP address.
		if json["attacker_ip_version"] == 4:
			json["attacker_ip_address"] = str(ipaddress.IPv4Address(data[9:13]))
		elif json["attacker_ip_version"] == 6:
			json["attacker_ip_address"] = str(ipaddress.IPv6Address(data[9:25]))
		else:
			json["attacker_ip_address"] = "IP UNKNOWN"

		# Discard the now-processed data.
		if json["attacker_ip_version"] == 4:
			data = data[13:]
		else:
			data = data[25:]

		# POST logging output.
		log(NORMAL, f"POST {ip}:{port}{api}")
		log(NORMAL, "| {")

		for k in json.keys():
			if type(json[k]) is str:
				log(NORMAL, f"|     \"{k}\": %s," % colored(f"\"{json[k]}\"", "yellow"))
			else:
				log(NORMAL, f"|     \"{k}\": %s," % colored(f"{json[k]}", "yellow"))

		log(NORMAL, "| }")

