import socket

def forward(db: str, sock: socket.socket, ip: str, port: int, api: str) -> None:
	"""
	Receive some data from the socket and forward it to the API endpoint
	in the form of JSON data.
	"""

	data = {
		# Time information.
		"epoch_timestamp"      : None,

		# Module information.
		"module_id"            : None,
		"module_name"          : None,
		"module_version"       : None,
		"module_description"   : None,

		# Attack information.
		"attack_type"          : None,
		"attack_desc"          : None,

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

