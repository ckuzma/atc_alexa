from util.object_parsing import ObjectParsing

class RadarInterpreter:
    def __init__(self, radar_blob):
        self.object_parsing = ObjectParsing()
        self.aircraft_list, self.lowest_aircraft = self.extract_aircraft(radar_blob['acList'])

    def extract_aircraft(self, raw_aircrafts):
        """
        We're only grabbing information that's useful (for now) but
        there is more that we could get and add some fun logic to in
        the future. Such as:

            Year    When the aircraft was built
            Reg     Tail number on the aircraft
            GAlt    Altitude at sea level
            Engines Number of engines on the aircraft
        """
        aircraft_list = []
        lowest_aircraft = None
        for aircraft in raw_aircrafts:
            aircraft_info = {
                'manufacturer': self.object_parsing.get_param(aircraft, 'Man'),
                'model': self.object_parsing.get_param(aircraft, 'Type'),
                'operator': self.object_parsing.get_param(aircraft, 'Op'),
                'flight_num': self.object_parsing.get_param(aircraft, 'Call'),
                'from': self.object_parsing.get_param(aircraft, 'From'),
                'to': self.object_parsing.get_param(aircraft, 'To'),
                'altitude': self.object_parsing.get_param(aircraft, 'Alt')
            }
            if aircraft_info['operator']: # Have to clean this up a bit
                operator = aircraft_info['operator']
                operator = operator.split('     ')
                aircraft_info['operator'] = operator[0]
            aircraft_list.append(aircraft_info)
            if lowest_aircraft is None and 'altitude' in aircraft_info and aircraft_info['altitude'] > 0:
                lowest_aircraft = aircraft_info
            if 'altitude' in aircraft_info and aircraft_info['altitude'] > 0 and aircraft_info['altitude'] < lowest_aircraft['altitude']:
                lowest_aircraft = aircraft_info
        return aircraft_list, lowest_aircraft
