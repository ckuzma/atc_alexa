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
        try:
            response = requests.get(GMAPS_URI, params=parameters).json()
        except:
            print('ERROR: Unable to communicate with Google API')
            return None, None, None
        if len(response['results']) == 0:
            return None, None, None
        location = response['results'][0]['geometry']['location']
        print('WARNING: Fix Google API usage, using dummy New York for name of location')
        return 'New York', location['lat'], location['lng']
