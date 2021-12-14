import hashlib
import ipaddress
import requests
import socket
import time

from lib.auxiliary import *
from lib.CacheDB import *
from lib.ipgeo import *
from lib.ModuleDB import *
from lib.traceroute import *
from termcolor import colored

def forward(
	db: ModuleDB, cache: CacheDB, sock: socket.socket, hostKey: str, selfIP: str,
	proto: str, ip: str, port: int, api: str
) -> None:
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
			# Host key.
			"host_key"             : None,

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

			# Traceroute information.
			"traceroute"           : None,
		}

		# Host information. To prevent the chance of a collision with another
		# host, the host key is hashed with the host IP.
		json["host_key"] = hashlib.sha1((hostKey+selfIP).encode()).hexdigest()

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

		# Victim IP version.
		if "." in selfIP:
			json["victim_ip_version"] = 4
		elif ":" in selfIP:
			json["victim_ip_version"] = 6
		else:
			json["victim_ip_version"] = -1

		# Victim IP address.
		json["victim_ip_address"] = selfIP

		# Get the victim coordinates, first checking the cache.
		if q:=cache.session.query(cache.IP).filter_by(ip=selfIP).first():
			json["victim_lat"] = q.latitude
			json["victim_lon"] = q.longitude
		else:
			json["victim_lat"], json["victim_lon"] = ipgeo(selfIP)
			cache.session.add(cache.IP(
				json["victim_ip_address"], json["victim_lat"], json["victim_lon"]))
			cache.session.commit()

		# Attacker IP version.
		json["attacker_ip_version"] = int(data[8])

		# Attacker IP address.
		if json["attacker_ip_version"] == 4:
			json["attacker_ip_address"] = str(ipaddress.IPv4Address(data[9:13]))
		elif json["attacker_ip_version"] == 6:
			json["attacker_ip_address"] = str(ipaddress.IPv6Address(data[9:25]))
		else:
			json["attacker_ip_address"] = "IP UNKNOWN"

		# Get the attacker coordinates and traceroute, first checking the cache.
		if q:=cache.session.query(cache.IP).filter_by(ip=json["attacker_ip_address"]).first():
			json["attacker_lat"]  = q.latitude
			json["attacker_lon"]  = q.longitude
			json["traceroute"]    = q.traceroute

		else:

			json["attacker_lat"], json["attacker_lon"] = ipgeo(json["attacker_ip_address"])
			json["traceroute"] = {}
			route = traceroute(json["attacker_ip_address"])

			# Either pull from cache or get+push to cache the intermediate hop coordinates.
			for hop in route.keys():
				if route[hop] == "?":
					json["traceroute"][hop] = {route[hop]: ("?", "?")}
				elif q:=cache.session.query(cache.IP).filter_by(ip=route[hop]).first():
					json["traceroute"][hop] = {route[hop]: (q.latitude, q.longitude)}
				else:
					hopCoordinates = ipgeo(route[hop])
					json["traceroute"][hop] = {route[hop]: hopCoordinates}
					cache.session.add(cache.IP(
						route[hop], hopCoordinates[0], hopCoordinates[1]))
					cache.session.commit()

			cache.session.add(cache.IP(
				json["attacker_ip_address"], json["attacker_lat"], json["attacker_lon"], json["traceroute"]))
			cache.session.commit()

		# Discard the now-processed data.
		if json["attacker_ip_version"] == 4:
			data = data[13:]
		else:
			data = data[25:]

		# POST to the API endpoint.
		r = requests.post(f"{proto}://{ip}:{port}{api}", json=json)

		# Check the status code.
		if r.status_code != 200:
			log(WARNING, f"POST request to {ip}:{port}{api} got status code {r.status_code}")
			return FAILURE

		# POST logging output.
		log(NORMAL, f"POST {ip}:{port}{api}")
		log(NORMAL, "| {")

		for k in json.keys():
			if type(json[k]) is str:
				log(NORMAL, f"|     \"{k}\": %s," % colored(f"\"{json[k]}\"", "yellow"))
			elif type(json[k]) is dict:
				log(NORMAL, f"|     \"{k}\":")
				log(NORMAL, f"|      %s" % colored("{", "yellow"))
				for subk in json[k].keys():
					log(NORMAL, f"|          %s %s%s" % (
						colored(f"{subk}:", "yellow"), colored(json[k][subk], "red"),
						colored(f",", "yellow")))
				log(NORMAL, f"|      %s," % colored("}", "yellow"))
			else:
				log(NORMAL, f"|     \"{k}\": %s," % colored(f"{json[k]}", "yellow"))

		log(NORMAL, "| }")

