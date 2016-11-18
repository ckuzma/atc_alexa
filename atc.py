from api.google_maps import GoogleMaps
from api.virtual_radar import VirtualRadar
from util.object_parsing import ObjectParsing
from util.radar_interpreter import RadarInterpreter

DISTANCE_RADIUS = 20, # Distance radius (2-dimensional) max
MAX_ALTITUDE = 40000 # Maximum Altitude

class AirTrafficControl:
    def __init__(self):
        self.virtual_radar = VirtualRadar()
        self.google_maps = GoogleMaps()
        self.response_builder = ResponseBuilder()
        self.location = None
        self.lat = None
        self.lon = None

    def save_location(self, location):
        self.location = location
        self.lat, self.lon = self.google_maps.location_from_address(location)
        return self.response_builder.saved_location(location)

    def whats_lowest_aircraft(self):
        if self.lat is None or self.lat is None:
            return self.response_builder.no_location_given()
        radar_scan = self.virtual_radar.get_aircraft(self.lat, self.lon, DISTANCE_RADIUS, MAX_ALTITUDE)
        results = RadarInterpreter(radar_scan)
        return self.response_builder.craft_result_response(results.lowest_aircraft, self.location)


class ResponseBuilder:
    def __init__(self):
        self.object_parsing = ObjectParsing()

    def craft_result_response(self, lowest_aircraft, location):
        if not lowest_aircraft:
            return 'There are currently no aircraft on radar near ' + location + '.'
        else:
            response_text = 'The lowest aircraft overhead'
            if self.object_parsing.get_param(lowest_aircraft, 'operator'):
                response_text += 'is a '
                response_text += lowest_aircraft['operator']
            if self.object_parsing.get_param(lowest_aircraft, 'manufacturer'):
                response_text += ' '
                response_text += lowest_aircraft['manufacturer']
            if self.object_parsing.get_param(lowest_aircraft, 'model'):
                response_text += ' '
                response_text += lowest_aircraft['model']
            if response_text == 'The lowest aircraft overhead': # If we got no aircraft information
                response_text += ' has no public information and is'
            response_text += ' at '
            response_text += str(lowest_aircraft['altitude'])
            response_text += ' feet within '
            response_text += '20' # XXX Needs to match DISTANCE_RADIUS
            response_text += ' kilometers of ' + location + '.'
            return response_text

    def no_location_given(self):
        response_text = 'I don\'t have your location! Tell me where you are.'
        return response_text

    def saved_location(self, location):
        response_text = 'Great! I have your location as '
        response_text += str(location)
        response_text += '.'
        return response_text

if __name__ == '__main__':
    print('\n\n\tRunning demonstration...\n')

    atc = AirTrafficControl()
    print(atc.save_location('new york new york'))
    print(atc.whats_lowest_aircraft())

    print('\n\tDone running demonstration!\n\n')
