import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
from config import DISTANCEMATRIX_API_KEY

key=DISTANCEMATRIX_API_KEY
def get_distance_matrix(api_key, origins, destinations):
    # Construct the URL for the Distance Matrix API
    url = f'https://maps.googleapis.com/maps/api/distancematrix/json?origins={origins}&destinations={destinations}&key={api_key}'

    # Set up retry mechanism
    retries = Retry(total=3, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504])
    session = requests.Session()
    session.mount('https://', HTTPAdapter(max_retries=retries))
    
    try:
        # Make the request to the Distance Matrix API
        response = session.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

# Example usage
api_key = DISTANCEMATRIX_API_KEY
origins = 'Juja'  # Replace with actual origin coordinates or addresses
destinations = 'Nairobi'  # Replace with actual destination coordinates or addresses

result = get_distance_matrix(api_key, origins, destinations)

if result:
    # Process the result as needed
    print(result)
else:
    print("Request to Google Maps Distance Matrix API failed.")
