import requests
from dotenv import load_dotenv
import os

class DataManager:
    #This class is responsible for talking to the Google Sheet.
    def __init__(self):
        load_dotenv(dotenv_path=".env")
        self.endpoint = os.getenv("SHEETY_ENDPOINT")
        self.__token = os.getenv("SHEETY_TOKEN")
        self.__headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.__token}"
        }

    def flight_sheet_data(self) -> list:
        response = requests.get(url=self.endpoint, headers=self.__headers)
        response.raise_for_status()
        return response.json().get("prices")

    def update_row(self, content):
        body = {
            "price": content
        }
        response = requests.put(url=f"{self.endpoint}/{content['id']}", headers=self.__headers, json=body)
        response.raise_for_status()
        print(response.json())
