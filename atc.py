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

    def get_lowest_aircraft(self, user_location_string):
        location, latitude, longitude = self.google_maps.location_from_address(user_location_string)
        if location is None:
            print('WARNING: Unable to lookup a location')
            return None
        else:
            try:
                radar_scan = self.virtual_radar.get_aircraft(latitude, longitude, DISTANCE_RADIUS, MAX_ALTITUDE)
                results = RadarInterpreter(radar_scan)
                return self.response_builder.craft_result_response(results.lowest_aircraft, location)
            except:
                print('ERROR: Unable to get virtual radar')
            return False

class ResponseBuilder:
    def __init__(self):
        self.object_parsing = ObjectParsing()

    def craft_result_response(self, lowest_aircraft, location):
        if not lowest_aircraft:
            return 'There are currently no aircraft on radar near ' + location + '.'
        else:
            response_text = 'The lowest aircraft over ' + location + ' '
            if self.object_parsing.get_param(lowest_aircraft, 'operator'):
                response_text += 'is a '
                response_text += lowest_aircraft['operator']
            if self.object_parsing.get_param(lowest_aircraft, 'manufacturer'):
                response_text += ' '
                response_text += lowest_aircraft['manufacturer']
            if self.object_parsing.get_param(lowest_aircraft, 'model'):
                response_text += ' '
                response_text += lowest_aircraft['model']
            if response_text == 'The lowest aircraft over ' + location + ' ': # If we got no aircraft information
                response_text += 'has no public information and is'
            response_text += ' at '
            response_text += str(lowest_aircraft['altitude'])
            response_text += ' feet.'
            return response_text

if __name__ == '__main__':
    print('\n\n\tRunning demonstration...\n')

    atc = AirTrafficControl()
    print(atc.get_lowest_aircraft('Blimey'))

    print('\n\tDone running demonstration!\n\n')
