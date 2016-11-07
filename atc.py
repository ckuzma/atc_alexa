import json

from api.virtual_radar import VirtualRadar
from util.location_lookup import LocationLookup
from util.object_parsing import ObjectParsing
from util.radar_interpreter import RadarInterpreter

DISTANCE_RADIUS = 20, # Distance radius (2-dimensional) max
MAX_ALTITUDE = 40000 # Maximum Altitude

class AirTrafficControl:
    def __init__(self):
        self.virtual_radar = VirtualRadar()
        self.location_lookup = LocationLookup()
        self.response_builder = ResponseBuilder()
        self.zipcode = None
        self.lat = None
        self.lon = None

    def whats_lowest_aircraft(self):
        if self.zipcode is None:
            self.response_builder.no_location()
            self.zipcode = '10016'
            self.lat, self.lon = self.location_lookup.location_from_zip(self.zipcode)
        radar_scan = self.virtual_radar.get_aircraft(self.lat, self.lon, DISTANCE_RADIUS, MAX_ALTITUDE)
        results = RadarInterpreter(radar_scan)
        return self.response_builder.craft_result_response(results.lowest_aircraft)

    def save_location(self):
        ## TODO: Make this work
        pass

class ResponseBuilder:
    def __init__(self):
        self.object_parsing = ObjectParsing()

    def craft_result_response(self, lowest_aircraft):
        response_text = 'There is currently'
        if self.object_parsing.get_param(lowest_aircraft, 'operator'):
            response_text += ' a '
            response_text += lowest_aircraft['operator']
        if self.object_parsing.get_param(lowest_aircraft, 'manufacturer'):
            response_text += ' '
            response_text += lowest_aircraft['manufacturer']
        if self.object_parsing.get_param(lowest_aircraft, 'model'):
            response_text += ' '
            response_text += lowest_aircraft['model']
        response_text += ' at '
        response_text += str(lowest_aircraft['altitude'])
        response_text += ' feet above the ground nearby.'
        return response_text

    def no_location(self):
        print('Oops! We need your zipcode. Continuing with dummy data for NYC for now...')

"""
Tests
"""

atc = AirTrafficControl()
response = atc.whats_lowest_aircraft()
print(response)
