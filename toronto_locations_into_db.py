import mysql.connector
from urllib.request import urlopen
import json
import http.client

def jsonDefault(object):
	return object.__dict__

class Location:
	def __init__(self, name, latitude, longitude, category=None):
		self.name = name
		self.latitude = latitude
		self.longitude = longitude
		self.category = category

def getLocations():
	location_list = []
	url = urlopen('http://app.toronto.ca/opendata//ac_locations/locations.json?v=1.00').read().decode('utf8')
	file = json.loads(url)
	for location in file:
		location_list.append(Location(location['locationName'], location['lat'], location['lon'], location['locationDesc']))
	return location_list


locations = getLocations()

conn = http.client.HTTPConnection("localhost:8000")
headers = {'content-type': "application/json"}

for i in range(len(locations)):
	payload = json.dumps({"name" : locations[i].name, "latitude": locations[i].latitude, "longitude": locations[i].longitude, "category": locations[i].category}, 
						indent=4, sort_keys=True, default=jsonDefault)
	conn.request("POST", "/rest_api/locations/", payload, headers)
	res = conn.getresponse()
	data = res.read()