"""
================
--  Templates --
================

EN-US
0.) There are {no} aircraft over {Portland} on our radar right now.
1.) There is {one} aircraft over {Portland} on our radar.
2.) There are {three} aircraft over {Portland} on our radar.
3.) There are {no} {airplanes} over {Portland} on our radar right now.
4.) There is {only one} {airplane} over {Portland} on our radar.
5.) There is {a single} {airplane} over {Portland} on our radar.
6.) There is {one} {airplane} and {two} {helicopters} over {Portland} on our radar.
7.) There are {two} {airplanes}, {one} {seaplane}, and {one} {helicopter} over {Portland} on our radar.

EN-UK
0.) There are {no} aircraft over {Portland} on our radar right now.
1.) There is {one} aircraft over {Portland} on our radar.
2.) There are {three} aircraft over {Portland} on our radar.
3.) There are {no} {aeroplanes} over {Portland} on our radar right now.
4.) There is {only one} {aeroplane} over {Portland} on our radar.
5.) There is {a single} {aeroplane} over {Portland} on our radar.
6.) There is {one} {aeroplane} and {two} {helicopters} over {Portland} on our radar.
7.) There are {two} {aeroplanes}, {one} {seaplane}, and {one} {helicopter} over {Portland} on our radar.

DE-DE
0.) Es gibt momentan {keine} Flugmaschine über {Portland} auf unserem Radar.
1.) Es gibt {eine} Flugmaschine über {Portland} auf unserem Radar.
2.) Es gibt {drei} Flugmaschinen über {Portland} auf unserem Radar.
3.) Es gibt momentan {keine} {Flugzeuge} über {Portland} auf unserem Radar.
4.) Es gibt {nur ein} {Flugzeug} über {Portland} auf unserem Radar.
5.) Es gibt {ein} {Flugzeug} über {Portland} auf unserem Radar.
6.) Es gibt {ein} {Flugzeug} und {zwei} {Hubschrauber} über {Portland} auf unserem Radar.
7.) Es gibt {zwei} {Flugzeuge}, {ein} {Wasserflugzeug}, und {einen} {Hubschrauber} über {Portland} auf unserem Radar.
"""

class ResponseGenerator:
    def __init__(self, lang):
        self.lang = lang
        self.generate_static()
    
    def generate_aircraft_details(self, craft):
        return_string = []
        if self.lang == 'de-de':
            return_string.append('ein')
        if self.lang == 'en-uk':
            return_string.append('a')
        if self.lang == 'en-us':
            return_string.append('a')
        if 'operator' in craft and craft['operator'] != None:
            return_string.append(craft['operator'])
        if 'manufacturer' in craft and craft['manufacturer'] != None:
            return_string.append(craft['manufacturer'])
        if 'model' in craft and craft['model'] != None:
            return_string.append(craft['model'])
        if self.lang == 'de-de':
            return_string.append('mit einer Flughöhe von')
        if self.lang == 'en-uk':
            return_string.append('at an altitude of')
        if self.lang == 'en-us':
            return_string.append('at an altitude of')
        return_string.append(str(craft['altitude']))
        if self.lang == 'de-de':
            return_string.append('Fuß')
        if self.lang == 'en-uk':
            return_string.append('feet')
        if self.lang == 'en-us':
            return_string.append('feet')
        return ' '.join(return_string)

    def generate_aircraft(self, craft_type, number):
        aircraft_nouns = {
            'de-de' : [
                ['Flugmaschine', 'Flugmaschinen'], # f
                ['Flugzeug', 'Flugzeuge'], # n
                ['Wasserflugzeug', 'Wasserflugzeuge'], # n
                ['Amphibienflugzeug', 'Amphibienflugzeuge'], # n
                ['Hubschrauber', 'Hubschrauber'], # m
                ['Tragschrauber', 'Tragschrauber'], # m
                ['VTOL-Flugzeug', 'VTOL-Flugzeuge'], # n
                ['Landfahrzeug', 'Landfahrzeuge'], # n
                ['Turm', 'Türme'] # m
            ],
            'en-uk' : [
                ['aircraft', 'aircraft'],
                ['aeroplane', 'aeroplanes'],
                ['seaplane', 'seaplanes'],
                ['amphibious aircraft', 'amphibious aircraft'],
                ['helicopter', 'helicopters'],
                ['gyrocopter', 'gyrocopters'],
                ['tiltwing', 'tiltwings'],
                ['ground vehicle', 'ground vehicles'],
                ['tower', 'towers']
            ],
            'en-us' : [
                ['aircraft', 'aircraft'],
                ['airplane', 'airplanes'],
                ['seaplane', 'seaplanes'],
                ['amphibious aircraft', 'amphibious aircraft'],
                ['helicopter', 'helicopters'],
                ['gyrocopter', 'gyrocopters'],
                ['tiltwing', 'tiltwings'],
                ['ground vehicle', 'ground vehicles'],
                ['tower', 'towers']
            ]
        }
        if number == 1:
            return aircraft_nouns[self.lang][craft_type][0]
        else:
            return aircraft_nouns[self.lang][craft_type][1]
    
    def generate_aircraft_count(self, aircraft_type, aircraft_count):
        """
        Accepts two integers, and returns a properly formatted output
        string consisting of the count and aircraft in that language:
            Examples:
                INPUT:  0, 0
                OUTPUT: 'no aircraft'

                INPUT:  1, 0
                OUTPUT: '0 airplanes'

                INPUT:  0, 0
                OUTPUT: 'keine Flugmaschinen'
        """
        ## German rules
        if self.lang == 'de-de':
            if aircraft_count == 0:
                return 'keine ' + self.generate_aircraft(aircraft_type, aircraft_count)
            if aircraft_count == 1:
                ## Refer to the aircraft index numbers for this
                if aircraft_type == 0:
                    return 'eine ' + self.generate_aircraft(aircraft_type, aircraft_count)
                if aircraft_type in [4, 5, 8]:
                    return 'einen ' + self.generate_aircraft(aircraft_type, aircraft_count)
                else:
                    return 'ein ' + self.generate_aircraft(aircraft_type, aircraft_count)
            else:
                return str(aircraft_count) + ' ' + self.generate_aircraft(aircraft_type, aircraft_count)
        ## English
        else:
            if aircraft_count == 0:
                return 'no ' + self.generate_aircraft(aircraft_type, aircraft_count)
            else:
                return str(aircraft_count) + ' ' + self.generate_aircraft(aircraft_type, aircraft_count)

    def generate_list(self, aircraft_list):
        """
        Accepts a list of aircraft in the following format:
        [
            [aircraft_type, aircraft_count],
            [aircraft_type, aircraft_count]
        ]
        aircraft_type = int (corresponds to type)
        aircraft_count = int (# of that type of aircraft)

        Returns the list as a nicely formatted string.
        """
        output_strings = []
        for aircraft in aircraft_list:
            output_strings.append(self.generate_aircraft_count(aircraft[0], aircraft[1]))
        if len(output_strings) == 0:
            return ''
        if len(output_strings) == 1:
            return output_strings[0]
        if len(output_strings) > 1:
            ## German
            if self.lang == 'de-de':
                output_strings[len(output_strings) - 1] = 'und ' + output_strings[len(output_strings) - 1]
            ## English
            else:
                output_strings[len(output_strings) - 1] = 'and ' + output_strings[len(output_strings) - 1]
        if len(output_strings) == 2:
            return ' '.join(output_strings)
        else:
            return ', '.join(output_strings)
            
    def generate_static(self):
        self.static = {}
        if self.lang == 'de-de':
            self.static['goodbye_title'] = 'ATC - Tschüss'
            self.static['goodbye_response'] = 'Auf Wiedersehen von Air Traffic Control!'
            self.static['hello_title'] = 'ATC - Grüße'
            self.static['hello_response'] = 'Ait Traffic Control. Du kannst mich fragen, was über einen Ort fliegt.'
            self.static['radar_title'] = 'ATC - Radar Lookup'
            self.static['radar_response'] = 'Du kannst eine Anfrage stellen, oder sag \"Stop\" oder \"Ende\" zu beenden.'
            self.static['radar_reprompt_1'] = 'Du hast keineen gültigen Ort eingegeben. Bitte versuch nochmal.'
            self.static['radar_reprompt_2'] = 'Ich habe den Ort nicht erkannt. Versuch nochmal. Zum Beispiel: Was fliegt über Berlin?'
            self.static['craft_type_error'] = 'Ich haben den Flugzeugtyp nicht erkannt. Versuch nochmal.'
        if self.lang == 'en-uk':
            self.static['goodbye_title'] = 'ATC - Goodbye'
            self.static['goodbye_response'] = 'Happy travels from Air Traffic Control!'
            self.static['hello_title'] = 'ATC - Welcome'
            self.static['hello_response'] = 'Air Traffic Control. You can ask me what is flying over any location.'
            self.static['radar_title'] = 'ATC - Radar Search'
            self.static['radar_response'] = 'You can make a request, or say \"Quit\" or \"Cancel\" to exit.'
            self.static['radar_reprompt_1'] = 'You did not give a valid location. Please try again.'
            self.static['radar_reprompt_2'] = 'I did not recognize a location. Try something like: What is flying over London.'
            self.static['craft_type_error'] = 'I did not recognize the type of aircraft you were asking about, please try again.'
        if self.lang == 'en-us':
            self.static['goodbye_title'] = 'ATC - Goodbye'
            self.static['goodbye_response'] = 'Happy travels from Air Traffic Control!'
            self.static['hello_title'] = 'ATC - Welcome'
            self.static['hello_response'] = 'Air Traffic Control. You can ask me what is flying over any location.'
            self.static['radar_title'] = 'ATC - Radar Search'
            self.static['radar_response'] = 'You can make a request, or say \"Quit\" or \"Cancel\" to exit.'
            self.static['radar_reprompt_1'] = 'You did not give a valid location. Please try again.'
            self.static['radar_reprompt_2'] = 'I did not recognize a location. Try something like: What is flying over New York.'
            self.static['craft_type_error'] = 'I did not recognize the type of aircraft you were asking about, please try again.'

"""
============
--  Tests --
============
"""
# if __name__ == '__main__':
#     airplanes = [
#         [0, 1],
#         [1, 0],
#         [2, 2],
#         [2, 1]
#     ]

#     print('-- US ENGLISH TEST --')
#     generator = ResponseGenerator('en-us')
#     print(generator.generate_list(airplanes))

#     print('-- UK ENGLISH TEST --')
#     generator = ResponseGenerator('en-uk')
#     print(generator.generate_list(airplanes))

#     print('-- DE GERMAN TEST --')
#     generator = ResponseGenerator('de-de')
#     print(generator.generate_list(airplanes))

