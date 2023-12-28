# flight_search.py
import requests

class FlightSearch:
    def __init__(self, api_key):
        self.api_key = api_key

    def get_iata_code(self, city_name):
        search_url = "https://api.tequila.kiwi.com/locations/query"
        headers = {
            "apikey": self.api_key,
        }
        params = {
            "term": city_name,
        }

        response = requests.get(search_url, headers=headers, params=params)

        if response.status_code == 200:
            data = response.json()
            locations = data.get("locations", [])
            if locations:
                return locations[0].get("code", "N/A")
            else:
                return "N/A"
        else:
            # Handle API request error
            print(f"Error fetching IATA code for {city_name}. Status code: {response.status_code}")
            return "N/A"

    def get_flight_price(self, source_code, destination_code):
        search_url = "https://api.tequila.kiwi.com/v2/search"
        headers = {
            "apikey": self.api_key,
        }
        params = {
            "fly_from": source_code,
            "fly_to": destination_code,
        }

        response = requests.get(search_url, headers=headers, params=params)

        if response.status_code == 200:
            data = response.json()
            prices = data.get("data", [])
            if prices:
                return prices[0].get("price", "N/A")
            else:
                return "N/A"
        else:
            # Handle API request error
            print(f"Error fetching flight price from {source_code} to {destination_code}. Status code: {response.status_code}")
            return "N/A"

    def search_direct_flights(self, origin, destination, departure_date, return_date):
        search_url = "https://api.tequila.kiwi.com/v2/search"
        headers = {
            "apikey": self.api_key,
        }
        params = {
            "fly_from": origin,
            "fly_to": destination,
            "date_from": departure_date,
            "date_to": return_date,
            "direct_flights": 1,
        }

        response = requests.get(search_url, headers=headers, params=params)

        if response.status_code == 200:
            data = response.json()
            options = data.get("data", [])
            return options
        else:
            # Handle API request error
            print(f"Error fetching direct flights from {origin} to {destination}. Status code: {response.status_code}")
            return []
