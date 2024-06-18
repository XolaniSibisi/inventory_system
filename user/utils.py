import requests

api_key = 'AIzaSyAiRFgP00JifQMC-mDCp3Pl26325BNTG9s'

def geocode_address(api_key, address):
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": address,
        "key": api_key
    }
    response = requests.get(url, params=params)
    data = response.json()
    # logging.debug(f"Geocoding response: {data}")
    if 'results' in data and data['results']:
        location = data['results'][0]['geometry']['location']
        latitude = location['lat']
        longitude = location['lng']
        return latitude, longitude
    else:
        return None, None
