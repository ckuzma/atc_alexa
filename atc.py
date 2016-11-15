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

    def save_location(self, zipcode):
        self.lat, self.lon = self.location_lookup.location_from_zip(zipcode)
        return self.response_builder.saved_location(zipcode)

    def whats_lowest_aircraft(self):
        if self.lat is None or self.lat is None:
            return self.response_builder.no_location_given()
        radar_scan = self.virtual_radar.get_aircraft(self.lat, self.lon, DISTANCE_RADIUS, MAX_ALTITUDE)
        results = RadarInterpreter(radar_scan)
        return self.response_builder.craft_result_response(results.lowest_aircraft)


class ResponseBuilder:
    def __init__(self):
        self.object_parsing = ObjectParsing()

    def craft_result_response(self, lowest_aircraft):
        if not lowest_aircraft:
            return 'There are currently no aircraft on radar nearby.'
        else:
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
            if response_text == 'There is currently': # If we got no aircraft information
                response_text += ' an unidentified aircraft'
            response_text += ' at '
            response_text += str(lowest_aircraft['altitude'])
            response_text += ' feet within '
            response_text += '20' # XXX Needs to match DISTANCE_RADIUS
            response_text += ' kilometers of your location.'
            return response_text

    def no_location_given(self):
        response_text = 'I don\'t have your location! Tell me your zipcode.'
        return response_text

    def saved_location(self, zipcode):
        response_text = 'Great! I have your zipcode as '
        response_text += str(zipcode)
        response_text += '.'
        return response_text

if __name__ == '__main__':
    import time

    atc = AirTrafficControl()
    print(atc.whats_lowest_aircraft())
    print(atc.save_location('new york new york'))
    print(atc.whats_lowest_aircraft())
    print('Waiting 5 seconds...')
    time.sleep(5)
    print(atc.whats_lowest_aircraft())
    print('Waiting 5 seconds...')
    time.sleep(5)
    print(atc.whats_lowest_aircraft())
    print('Waiting 5 seconds...')
