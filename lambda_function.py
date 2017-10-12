from __future__ import print_function

## Import libraries
import json

## Import our classes...
from atc import AirTrafficControl

## Initialize our credentials class
from config import Credentials
credentials = Credentials()

## Import our static strings...
STATIC_STRINGS = json.loads(open('strings/static.json', 'r').read())

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

def get_welcome_response(lang):
    session_attributes = {}
    card_title = STATIC_STRINGS[lang]['hello_title']
    speech_output = STATIC_STRINGS[lang]['hello_response']
    reprompt_text = STATIC_STRINGS[lang]['hello_response']
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))

def handle_session_end_request(lang):
    card_title = STATIC_STRINGS[lang]['goodbye_title']
    speech_output = STATIC_STRINGS[lang]['goodbye_response']
    should_end_session = True
    return build_response({}, build_speechlet_response(card_title, speech_output, None, should_end_session))

def get_radar(intent, session, lang):
    card_title = STATIC_STRINGS[lang]['radar_title']
    session_attributes = {}
    if 'Location' in intent['slots'] and 'value' in intent['slots']['Location']:
        user_location = intent['slots']['Location']['value']
        speech_output = get_intent_speech(intent, user_location, lang)
        reprompt_text = STATIC_STRINGS[lang]['radar_response']
        should_end_session = True
    else:
        speech_output = STATIC_STRINGS[lang]['radar_reprompt_1']
        reprompt_text = STATIC_STRINGS[lang]['radar_reprompt_2']
        should_end_session = False
    return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))

def interpret_language(locale):
    if locale == 'de-DE':
        return 'de-de'
    if locale == 'en-UK':
        return 'en-uk'
    if local == 'en-US':
        return 'en-us'

def get_intent_speech(intent, location, lang):
    ## Instantiate our class w/language
    atc_control = AirTrafficControl(lang)

    ## Handle the specific intents
    if intent['name'] == 'AircraftCountIntent':
        return atc_control.aircraft_count(location)
    if intent['name'] == 'AircraftCountSpecificIntent':
        return atc_control.aircraft_count_specific(location)
    if intent['name'] == 'AircraftOfTypeIntent':
        craft_type = None
        craft_dict = {
            'airplanes': 1,
            'seaplanes': 2,
            'amphibians': 3,
            'helicopters': 4,
            'gyrocopters': 5,
            'tiltwings': 6,
            'ground vehicles': 7,
            'towers': 8
        }
        try:
            craft_type = craft_dict[intent['slots']['CraftType']['value']]
        except:
            pass
        if craft_type is not None:
            return atc_control.aircraft_of_type(location, craft_type)
        return STATIC_STRINGS[lang]['craft_type_error']
    if intent['name'] == 'HighestAircraftIntent':
        return atc_control.highest_aircraft(location)
    if intent['name'] == 'LowestAircraftIntent':
        return atc_control.lowest_aircraft(location)

def on_session_started(session_started_request, session):
    print("on_session_started requestId=" + session_started_request['requestId'] + ", sessionId=" + session['sessionId'])

def on_launch(launch_request, session):
    print("on_launch requestId=" + launch_request['requestId'] + ", sessionId=" + session['sessionId'])
    return get_welcome_response(launch_request['locale'])

def on_intent(intent_request, session):
    print("on_intent requestId=" + intent_request['requestId'] +", sessionId=" + session['sessionId'])
    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']
    intent_lang = intent_request['locale']
    custom_intents = [
        'AircraftCountIntent',
        'AircraftCountSpecificIntent',
        'AircraftOfTypeIntent',
        'HighestAircraftIntent',
        'LowestAircraftIntent'
    ]
    if intent_name in custom_intents:
        return get_radar(intent, session, intent_lang)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response(intent_lang)
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request(intent_lang)
    else:
        raise ValueError("Invalid intent")

def on_session_ended(session_ended_request, session):
    print("on_session_ended requestId=" + session_ended_request['requestId'] + ", sessionId=" + session['sessionId'])

def lambda_handler(event, context):
    ## Verify that the application ID matches what we expect
    print("event.session.application.applicationId=" + event['session']['application']['applicationId'])
    if (event['session']['application']['applicationId'] != credentials.alexa_id):
        raise ValueError("Invalid Application ID")

    ## Start the actual event handling
    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},event['session'])
    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])


"""
===========
-- Tests --
===========
"""

# if __name__ == '__main__':
#     ## Create a dummy event
#     dummy_event ={
#         "session": {
#             "new": True,
#             "sessionId": "SessionId.xxxx",
#             "application": {
#             "applicationId": ""
#             },
#             "attributes": {},
#             "user": {
#             "userId": "amzn1.ask.account.xxxx"
#             }
#         },
#         "request": {
#             "type": "IntentRequest",
#             "requestId": "EdwRequestId.xxxx",
#             "intent": {
#                 "name": "",
#                 "slots": {
#                     "CraftType": {
#                         "name": "CraftType",
#                         "value": "helicopters"
#                     },
#                     "Location": {
#                         "name": "Location",
#                         "value": "Portland"
#                     }
#                 }
#             },
#             "locale": "",
#             "timestamp": "2017-10-10T01:23:50Z"
#         },
#         "context": {
#             "AudioPlayer": {
#             "playerActivity": "IDLE"
#             },
#             "System": {
#             "application": {
#                 "applicationId": "amzn1.ask.skill.xxxx"
#             },
#             "user": {
#                 "userId": "amzn1.ask.account.xxxx"
#             },
#             "device": {
#                 "supportedInterfaces": {}
#             }
#             }
#         },
#         "version": "1.0"
#     }
#     dummy_event['session']['application']['applicationId'] = credentials.alexa_id

#     ## Set the params
#     dummy_event['request']['locale'] = 'en-UK'
#     dummy_event['request']['intent']['slots']['CraftType']['value'] = 'helicopters' # <-- Not used by every intent
#     dummy_event['request']['intent']['slots']['Location']['value'] = 'New York'

#     ## Set the intent
#     # dummy_event['request']['intent']['name'] = 'AircraftCountIntent'
#     # dummy_event['request']['intent']['name'] = 'AircraftCountSpecificIntent'
#     # dummy_event['request']['intent']['name'] = 'AircraftOfTypeIntent'
#     # dummy_event['request']['intent']['name'] = 'HighestAircraftIntent'
#     dummy_event['request']['intent']['name'] = 'LowestAircraftIntent'

    ## Execute the Lambda handler
    response = lambda_handler(dummy_event, None) # <-- We don't need context where we're going
    print('\n--- [ DEBUG RESULTS: ] ----')
    print(response['response']['outputSpeech']['text'])
    print('---------------------------\n')
    