class LocationUtils:
    def parse_useful_bits(self, location_blob):
        if len(location_blob['results']) == 0:
            return None
        else:
            useful_bits = {
                'name': location_blob['results'][0]['address_components'][0]['long_name'],
                'lat': location_blob['results'][0]['geometry']['location']['lat'],
                'lon': location_blob['results'][0]['geometry']['location']['lng']
            }
            return useful_bits
