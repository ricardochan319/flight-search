# data_manager.py
import requests

class DataManager:
    def __init__(self, base_url):
        self.base_url = base_url

    def update_row(self, row_id, data):
        update_url = f"{self.base_url}/{row_id}"
        response = requests.put(update_url, json=data)
        return response
