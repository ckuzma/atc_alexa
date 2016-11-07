import json

from api.virtual_radar import VirtualRadar

## Virtual Radar
virtual_radar = VirtualRadar()
print(json.dumps(virtual_radar.get_aircraft(40.7128, -74.0059, 20, 40000), indent=2))
