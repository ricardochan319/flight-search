# main.py
import requests
from datetime import datetime, timedelta
from flight_search import FlightSearch
from data_manager import DataManager
from user_input import get_user_input, add_user_to_sheet

# Get user input at the very beginning
print("Welcome! Please provide the following information:")
first_name, last_name, email = get_user_input()

# Call the function from user_input.py to add user information to the Google Sheet
add_user_to_sheet(first_name, last_name, email)

# Function to calculate the date in the future
def get_future_date(days):
    return (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d")

# Tequila Kiwi API
tequila_api_key = "JUFLTvy8P59qAnWTLqxMHMPJJzCJaA0O"
flight_search = FlightSearch(tequila_api_key)

# Sheety API
base_url = "https://api.sheety.co"
sheet_id = "e4c8cbdfafa8a258a3ba474487a4b92e"
endpoint = "flightTracker/prices"

url = f"{base_url}/{sheet_id}/{endpoint}"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    sheet_data = data.get('prices', [])

    # Instantiate the DataManager class with the base URL
    base_url = f"{base_url}/{sheet_id}/{endpoint}"
    data_manager = DataManager(base_url)

    # Check if the "iataCode" key is empty for any city
    for city_entry in sheet_data:
        if not city_entry.get("iataCode"):
            # Use FlightSearch class to get IATA code
            iata_code = flight_search.get_iata_code(city_entry["city"])

            # Update the sheet_data dictionary with the obtained IATA code
            city_entry["iataCode"] = iata_code

            # Update the Google Sheet using DataManager
            row_id = city_entry.get("id")
            if row_id:
                update_data = {"sheet1": city_entry}
                response = data_manager.update_row(row_id, update_data)
                if response.status_code == 200:
                    print(f"Row {row_id} updated successfully.")
                else:
                    print(f"Error updating row {row_id}. Status code: {response.status_code}")

    # Search for direct flight prices from origin to all destinations within the next 6 months
    rdu_code = flight_search.get_iata_code("Raleigh")
    if rdu_code != "N/A":
        for destination in sheet_data:
            destination_code = destination.get("iataCode", "N/A")
            if destination_code != "N/A":
                # Search for flight prices from origin to the destination
                departure_date = get_future_date(1)
                return_date = get_future_date(180)

                # Search for direct flights
                flight_options = flight_search.search_direct_flights(
                    rdu_code, destination_code, departure_date, return_date
                )

                if flight_options:
                    # Extract the lowest price from the options
                    lowest_price = min(option["price"] for option in flight_options)
                    print(f"{destination['city']}: {lowest_price}")
                else:
                    print(f"No direct flights found from Raleigh to {destination['city']}")
else:
    print(f"Error fetching data from Google Sheet. Status code: {response.status_code}")
