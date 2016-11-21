from atc import AirTrafficControl

atc_control = AirTrafficControl()

locations = [
    'portland',
    'denver',
    'new york',
    'barcelona',
    'cleveland',
    'narnia',
    'this shouldn\'t have a match',
]

print('\n\t----[ TEST: Lowest aircraft for location ]----')
for entry in locations:
    print(entry)
    print(atc_control.get_lowest_aircraft(entry))
    print('')

print('\n\t----[ TEST: Highest aircraft for location ]----')
for entry in locations:
    print(entry)
    print(atc_control.get_highest_aircraft(entry))
    print('')
