from __future__ import print_function

## Import our classes...
from atc import AirTrafficControl
from config import Credentials
from util.response_generator import ResponseGenerator

## Initialize our credentials class
credentials = Credentials()

## Instantiate global variables for use later
atc_control = None
generator = None

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': title,
            'content': output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }

def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }

def get_welcome_response():
    session_attributes = {}
    card_title = generator.static['hello_title']
    speech_output = generator.static['hello_response']
    reprompt_text = generator.static['hello_response']
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))

def handle_session_end_request():
    card_title = generator.static['goodbye_title']
    speech_output = generator.static['goodbye_response']
    should_end_session = True
    return build_response({}, build_speechlet_response(card_title, speech_output, None, should_end_session))

def get_radar(intent, session):
    card_title = generator.static['radar_title']
    session_attributes = {}
    if 'Location' in intent['slots'] and 'value' in intent['slots']['Location']:
        user_location = intent['slots']['Location']['value']
        speech_output = get_intent_speech(intent, user_location)
        reprompt_text = generator.static['radar_response']
        should_end_session = True
    else:
        speech_output = generator.static['radar_reprompt_1']
        reprompt_text = generator.static['radar_reprompt_2']
        should_end_session = False
    return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))

def interpret_language(locale):
    if locale == 'de-DE':
        return 'de-de'
    if locale == 'en-UK':
        return 'en-uk'
    if local == 'en-US':
        return 'en-us'

def get_intent_speech(intent, location):
    if intent['name'] == 'AircraftCountIntent':
        return atc_control.aircraft_count(location)
    if intent['name'] == 'AircraftCountSpecificIntent':
        return atc_control.aircraft_count_specific(location)
    if intent['name'] == 'AircraftOfTypeIntent':
        craft_type = None
        if intent['slots']['CraftType']['value'] == 'airplanes':
            craft_type = 1
        if intent['slots']['CraftType']['value'] == 'seaplanes':
            craft_type = 2
        if intent['slots']['CraftType']['value'] == 'amphibians':
            craft_type = 3
        if intent['slots']['CraftType']['value'] == 'helicopters':
            craft_type = 4
        if intent['slots']['CraftType']['value'] == 'gyrocopters':
            craft_type = 5
        if intent['slots']['CraftType']['value'] == 'tiltwings':
            craft_type = 6
        if intent['slots']['CraftType']['value'] == 'ground vehicles':
            craft_type = 7
        if intent['slots']['CraftType']['value'] == 'towers':
            craft_type = 8
        if craft_type is not None:
            return atc_control.aircraft_of_type(location, craft_type)
        return generator.static['craft_type_error']
    if intent['name'] == 'HighestAircraftIntent':
        return atc_control.highest_aircraft(location)
    if intent['name'] == 'LowestAircraftIntent':
        return atc_control.lowest_aircraft(location)

def on_session_started(session_started_request, session):
    print("on_session_started requestId=" + session_started_request['requestId'] + ", sessionId=" + session['sessionId'])

def on_launch(launch_request, session):
    print("on_launch requestId=" + launch_request['requestId'] + ", sessionId=" + session['sessionId'])
    return get_welcome_response()

def on_intent(intent_request, session):
    print("on_intent requestId=" + intent_request['requestId'] +", sessionId=" + session['sessionId'])
    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']
    custom_intents = [
        'AircraftCountIntent',
        'AircraftCountSpecificIntent',
        'AircraftOfTypeIntent',
        'HighestAircraftIntent',
        'LowestAircraftIntent'
    ]
    if intent_name in custom_intents:
        return get_radar(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")

def on_session_ended(session_ended_request, session):
    print("on_session_ended requestId=" + session_ended_request['requestId'] + ", sessionId=" + session['sessionId'])

def lambda_handler(event, context):
    print("event.session.application.applicationId=" + event['session']['application']['applicationId'])
    if (event['session']['application']['applicationId'] != credentials.alexa_id):
        raise ValueError("Invalid Application ID")
    generator = ResponseGenerator(interpret_language(event['request']['locale']))
    atc_control = AirTrafficControl(interpret_language(event['request']['locale']))
    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},event['session'])
    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
