import requests

RADAR_URL = 'http://public-api.adsbexchange.com/VirtualRadar/AircraftList.json'

class VirtualRadar:
    def get_aircraft(self, lat, lon, dist_radius, max_alt):
        parameters = {
            'lat': lat,
            'lng': lon,
            'fDstU': dist_radius, # Distance in kilometers
            'fAltU': max_alt # Altitude in feet
        }
        return requests.get(RADAR_URL, params=parameters).json()
