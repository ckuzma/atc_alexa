![Logo for Air Traffic Control](./misc/atc_icon_large_publish.png)

# atc_alexa
Air Traffic Control skill for Amazon Alexa. Gives information about what is flying over any location. Submitted as contest entry to the Alexa API Mashup competition on Hackster. (https://www.hackster.io/kuzma/alexa-air-traffic-control-a22a03)

## How It Works
Given a location (string) by a user, we query the Google Maps API for the approximate latitude and longitude corresponding to it. We then query the ADS-B Exchange for any radar data within a 20-kilometer radius and return information about the one flying the lowest.

## Future Work
* Aircraft filtering (E.g. "What's the highest helicopter near Rochester?" or "Are there any blimps in Tillamook?"
* Conditional filtering (E.g. "Is anything in Portland flying higher than 10,000 feet?")

## Instructions
1. Clone the repo
2. Get an API Key for the Google Maps Geocoding API. Go here for more information: https://developers.google.com/maps/documentation/geocoding/start
2. Modify the key values in `config.py.example` with your credentials. Open in an editor for more detailed instructions. (If not deploying to AWS Lambda, no need to modify the Alexa App ID.)
3. Execute the AirTrafficControl class (`python atc.py`) to make sure everything is working. Modify line 72 of `atc.py` with different location strings to test how that works.
4. If you want to deploy using AWS Lambda and the Alexa Skills Kit, zip all of the files and upload. See the Amazon Alexa developer portal (https://developer.amazon.com/alexa) for more information on how to deploy. Look in `/alexa` for the intent schema and training utterances.

## Credits
This project makes use of the following APIs:
* ADS-B Exchange, http://www.ADSBexchange.com
* Google Maps Geocoding API, https://developers.google.com
