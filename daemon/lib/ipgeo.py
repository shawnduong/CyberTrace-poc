import json
import requests

ENDPOINT = "http://ip-api.com/json/"

def ipgeo(ip: str) -> tuple:
	"""
	Geolocate an IP address and return (latitude: float, longitude: float).
	If no IP is given, also return self IP in addition to the coordinates. This
	uses ip-api.com.
	"""

	try:
		if len(ip) > 0:
			data = requests.get(ENDPOINT + ip).content.decode()
			jdat = json.loads(data)
			return (jdat["lat"], jdat["lon"])
		else:
			data = requests.get(ENDPOINT + ip).content.decode()
			jdat = json.loads(data)
			return (jdat["query"], jdat["lat"], jdat["lon"])
	except:
		return ("?", "?")

