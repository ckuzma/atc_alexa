import requests

from config import Credentials
credentials = Credentials()

API_KEY = credentials.gmap_key
GMAPS_URI = 'https://maps.googleapis.com/maps/api/geocode/json'

class GoogleMaps:
    def __init__(self):
        pass

    def location_from_address(self, zipcode):
        parameters = {
            'address': zipcode,
            'key': API_KEY
        }
        response = requests.get(GMAPS_URI, params=parameters).json()
        if len(response['results']) == 0:
            return None, None
        location = response['results'][0]['geometry']['location']
        return location['lat'], location['lng']
