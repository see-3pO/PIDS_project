import googlemaps
from datetime import datetime

def calculate_eta_with_traffic(origin, destination, mode, departure_time):
    gmaps = googlemaps.Client(key=API_KEY)
    try:
        result = gmaps.distance_matrix(origin, destination, mode=mode, departure_time=departure_time, traffic_model="best_guess")
        # Extract the duration with traffic from the result
        duration_with_traffic = result['rows'][0]['elements'][0]['duration_in_traffic']['text']
        return duration_with_traffic
    except googlemaps.exceptions.ApiError as e:
        print("ApiError: {0}".format(e))
        return None
    
calculate_eta_with_traffic()
