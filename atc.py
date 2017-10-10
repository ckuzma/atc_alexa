import json

from api.google_maps import GoogleMaps
from api.virtual_radar import VirtualRadar
from util.location_utils import LocationUtils
from util.object_parsing import ObjectParsing
from util.radar_interpreter import RadarInterpreter
from util.response_generator import ResponseGenerator

## Import the credentials
from config import Credentials
credentials = Credentials()

DISTANCE_RADIUS = 20, # Distance radius (2-dimensional) max
MAX_ALTITUDE = 80000 # Maximum Altitude

class AirTrafficControl:
    def __init__(self, language):
        self.lang = language
        self.virtual_radar = VirtualRadar()
        self.google_maps = GoogleMaps()
        self.location_utils = LocationUtils()
        self.radar_interpreter = RadarInterpreter()
        self.generator = ResponseGenerator(self.lang)

    def _get_location(self, user_location_string):
        """
        Returns a nice little object that has the latitude and
        longitude corresponding to the location from the user.
        """
        location = self.google_maps.location_from_address(user_location_string)
        if location == None:
            return None
        else:
            location = self.location_utils.parse_useful_bits(location)
            return location

    def _get_aircraft(self, user_location_string, debug=False):
        """
        Returns a list of all aircraft found for that location, or
        a null value if none are found or if an IO error.
        """
        location = self._get_location(user_location_string)
        if location == None:
            print('DEBUG: Unable to get user location (' + user_location_string + ')')
            return None
        radar_results = self.virtual_radar.get_radar(location['lat'], location['lon'], DISTANCE_RADIUS, MAX_ALTITUDE)
        if debug is True:
            print(json.dumps(radar_results, indent=2))
        if radar_results == None:
            print('DEBUG: Unable to get radar scan from API (' + user_location_string + ')')
            return None
        aircraft = self.radar_interpreter.extract_aircraft(radar_results['acList'])
        if len(aircraft) == 0:
            print('DEBUG: No aircraft overhead (' + location['name'] + ')')
            return None
        return aircraft

    def aircraft_count(self, user_location_string):
        """
        Counts the number of aircraft overhead. Returns a string.
        """
        aircraft = self._get_aircraft(user_location_string)
        response = self.generator.generate_list([[0, len(aircraft)]])
        ## German
        if self.lang == 'de-DE':
            return 'Momentan gibt es auf unserem Radar ' + response + ' über ' + user_location_string + '.'

        ## UK English
        if self.lang == 'en-UK' and len(aircraft) > 1:
            return 'There are ' + response + ' over ' + user_location_string + ' on our radar right now.'
        

        ## US English
        if self.lang == 'en-US':
            return 'There are ' + response + ' over ' + user_location_string + ' on our radar right now.'

    def aircraft_count_specific(self, user_location_string):
        """
        Note: This is kind of a messy function, but it's easier to read this way.

        Counts the number of each type of aircraft overhead. Returns a string.
        """
        aircraft = self._get_aircraft(user_location_string)
        landplanes = 0
        seaplanes = 0
        amphibians = 0
        helicopters = 0
        gyrocopters = 0
        tiltwings = 0
        if aircraft:
            for craft in aircraft:
                if craft['craft_type'] == 1:
                    landplanes+=1
                if craft['craft_type'] == 2:
                    seaplanes+=1
                if craft['craft_type'] == 3:
                    amphibians+=1
                if craft['craft_type'] == 4:
                    helicopters+=1
                if craft['craft_type'] == 5:
                    gyrocopters+=1
                if craft['craft_type'] == 6:
                    tiltwings+=1
        results_list = []
        if landplanes > 0:
            results_list.append([1, landplanes])
        if seaplanes > 0:
            results_list.append([2, seaplanes])
        if amphibians > 0:
            results_list.append([3, amphibians])
        if helicopters > 0:
            results_list.append([4, helicopters])
        if gyrocopters > 0:
            results_list.append([5, gyrocopters])
        if tiltwings > 0:
            results_list.append([6, tiltwings])
        if len(results_list) == 0:
            results_list.append([0, 0])
        response = self.generator.generate_list(results_list)
        if self.lang == 'de-DE':
            return 'Momentan gibt es auf unserem Radar ' + response + ' über ' + user_location_string + '.'
        if self.lang == 'en-UK':
            return 'There are ' + response + ' over ' + user_location_string + ' on our radar right now.'
        if self.lang == 'en-US':
            return 'There are ' + response + ' over ' + user_location_string + ' on our radar right now.'

    def aircraft_of_type(self, user_location_string, desired_type):
        """
        1 = Landplane
        2 = Seaplane
        3 = Amphibian
        4 = Helicopter
        5 = Gyrocopter
        6 = Tiltwing
        7 = GroundVehicle
        8 = Tower

        Returns a string.
        """
        aircraft = self._get_aircraft(user_location_string)
        response = None
        if aircraft:
            single_type = {'altitude': 0}
            type_count = 0
            for craft in aircraft:
                if craft['craft_type'] == desired_type:
                    if craft['altitude'] > single_type['altitude']:
                        single_type = craft
                type_count+=1
                response = self.generator.generate_list([[desired_type, type_count]])
        else:
            response = self.generator.generate_list([[0, 0]])
        if self.lang == 'de-DE':
            return 'Momentan gibt es auf unserem Radar ' + response + ' über ' + user_location_string + '.'
        if self.lang == 'en-UK':
            return 'There are ' + response + ' over ' + user_location_string + ' on our radar right now.'
        if self.lang == 'en-US':
            return 'There are ' + response + ' over ' + user_location_string + ' on our radar right now.'

    def highest_aircraft(self, user_location_string):
        """
        Gets information about the highest aircraft on radar. Returns a string.
        """
        aircraft = self._get_aircraft(user_location_string)
        response = None
        if aircraft:
            highest_craft = {'altitude': 0}
            for craft in aircraft:
                if craft['altitude'] > highest_craft['altitude']:
                    highest_craft = craft
            response = self.generator.generate_aircraft_details(highest_craft)
        else:
            response = self.generator.generate_list([[0, 0]])
        if self.lang == 'de-DE':
            return 'Momentan gibt es auf unserem Radar ' + response + ' über ' + user_location_string + '.'
        if self.lang == 'en-UK':
            return 'We found ' + response + ' over ' + user_location_string + ' on our radar right now.'
        if self.lang == 'en-US':
            return 'We found ' + response + ' over ' + user_location_string + ' on our radar right now.'

    def lowest_aircraft(self, user_location_string):
        """
        Gets information about the lowest aircraft on radar. Returns a string.
        """
        aircraft = self._get_aircraft(user_location_string)
        response = None
        if aircraft:
            lowest_craft = {'altitude': 500000} # Outer space begins at 264,000 feet
            for craft in aircraft:
                if craft['altitude'] < lowest_craft['altitude'] and craft['altitude'] > 0:
                    lowest_craft = craft
            response = self.generator.generate_aircraft_details(lowest_craft)
        else:
            response = self.generator.generate_list([[0, 0]])
        if self.lang == 'de-DE':
            return 'Momentan gibt es auf unserem Radar ' + response + ' über ' + user_location_string + '.'
        if self.lang == 'en-UK':
            return 'We found ' + response + ' over ' + user_location_string + ' on our radar right now.'
        if self.lang == 'en-US':
            return 'We found ' + response + ' over ' + user_location_string + ' on our radar right now.'


"""
Tests:
"""
# if __name__ == '__main__':
#     print('\n--- DE (DE) Tests --')
#     atc = AirTrafficControl('de-DE')
#     print(atc.aircraft_count('Los Angeles'))
#     print(atc.aircraft_count_specific('Los Angeles'))
#     print(atc.aircraft_of_type('Los Angeles', 1))
#     print(atc.highest_aircraft('Los Angeles'))
#     print(atc.lowest_aircraft('Los Angeles'))
    
#     print('\n--- EN (UK) Tests --')
#     atc = AirTrafficControl('en-UK')
#     print(atc.aircraft_count('Los Angeles'))
#     print(atc.aircraft_count_specific('Los Angeles'))
#     print(atc.aircraft_of_type('Los Angeles', 1))
#     print(atc.highest_aircraft('Los Angeles'))
#     print(atc.lowest_aircraft('Los Angeles'))

#     print('\n--- EN (US) Tests --')
#     atc = AirTrafficControl('en-US')
#     print(atc.aircraft_count('Los Angeles'))
#     print(atc.aircraft_count_specific('Los Angeles'))
#     print(atc.aircraft_of_type('Los Angeles', 1))
#     print(atc.highest_aircraft('Los Angeles'))
#     print(atc.lowest_aircraft('Los Angeles'))
