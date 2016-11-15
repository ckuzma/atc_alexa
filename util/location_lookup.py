import requests

API_KEY = '<PUT YOUR KEY HERE>'
GMAPS_URI = 'https://maps.googleapis.com/maps/api/geocode/json'

class LocationLookup:
    def __init__(self):
        pass

    def location_from_zip(self, zipcode):
        parameters = {
            'address': zipcode,
            'key': API_KEY
        }
        response = requests.get(GMAPS_URI, params=parameters).json()
        location = response['results'][0]['geometry']['location']
        return location['lat'], location['lng']
