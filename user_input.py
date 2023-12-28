import requests

BASE_URL = "https://api.sheety.co/"
API_KEY = "e4c8cbdfafa8a258a3ba474487a4b92e/"
ENDPOINT = "flightTracker/users"

SHEETY_API_URL = BASE_URL + API_KEY + ENDPOINT

def check_email_exists(email):
    params = {
        "filter[email]": email
    }

    response = requests.get(SHEETY_API_URL, params=params)
    data = response.json()

    if response.status_code == 200:
        return len(data['users']) > 0
    else:
        print(f"Error checking email: {response.status_code} - {response.text}")
        return False

def add_user_to_sheet(first_name, last_name, email):
    if check_email_exists(email):
        print(f"Error: Email '{email}' already exists in the database.")
        return

    headers = {
        "Content-Type": "application/json",
    }

    data = {
        "user": {
            "firstName": first_name,
            "lastName": last_name,
            "email": email,
        }
    }

    response = requests.post(SHEETY_API_URL, json=data, headers=headers)

    if response.status_code == 200:
        print("User information added successfully to the Google Sheet!")
    else:
        print(f"Error: {response.status_code} - {response.text}")

def get_user_input():
    first_name = input("Enter your first name: ")
    last_name = input("Enter your last name: ")

    while True:
        email = input("Enter your email address: ")
        confirm_email = input("Confirm your email address: ")

        if email == confirm_email:
            break
        else:
            print("Email addresses do not match. Please try again.")

    return first_name, last_name, email

if __name__ == "__main__":
    print("Welcome! Please provide the following information:")
    first_name, last_name, email = get_user_input()

    add_user_to_sheet(first_name, last_name, email)
