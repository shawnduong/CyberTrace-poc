import json
import requests

ENDPOINT = "http://ip-api.com/json/"

def ipgeo(ip: str) -> tuple:
	"""
	Geolocate an IP address and return (latitude: float, longitude: float).
	This uses ip-api.com.
	"""

	data = requests.get(ENDPOINT + ip).content.decode()
	jdat = json.loads(data)

	return (jdat["lat"], jdat["lon"])

