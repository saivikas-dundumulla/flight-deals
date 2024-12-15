from datetime import datetime

import requests
import os
from dotenv import load_dotenv


class FlightSearch:
    #This class is responsible for talking to the Flight Search API.
    def __init__(self):
        load_dotenv(dotenv_path=".env")
        self.__api_key = os.getenv("AMADEUS_API_KEY")
        self.__api_secret = os.getenv("AMADEUS_API_SECRET")
        self.endpoint = "https://test.api.amadeus.com/v2/shopping/flight-offers"
        self.token_endpoint = "https://test.api.amadeus.com/v1/security/oauth2/token"
        self.city_search_endpoint = "https://test.api.amadeus.com/v1/reference-data/locations/cities"
        self.__token = self.__access_token()

    def __access_token(self) -> str:
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {
            "grant_type": "client_credentials",
            "client_id": self.__api_key,
            "client_secret": self.__api_secret
        }
        response = requests.post(url=self.token_endpoint, headers=headers, data=data)
        response.raise_for_status()
        return response.json().get("access_token")

    def flight_search(self, origin_code:str, dest_code:str, departure_date:datetime, return_date:datetime, adults:int, **kwargs):
        oauth_token = self.__token
        from_date = departure_date.strftime(format="%Y-%m-%d")
        to_date = return_date.strftime(format="%Y-%m-%d")
        headers = {
            "Authorization": f"Bearer {oauth_token}"
        }
        search_criteria = {
            "originLocationCode": origin_code,
            "destinationLocationCode": dest_code,
            "departureDate": from_date,
            "adults": adults,
            "returnDate": to_date,
            **kwargs
        }
        response = requests.get(url=self.endpoint, params=search_criteria, headers=headers)
        response.raise_for_status()
        return response.json()

    def city_search(self, city):
        oauth_token = self.__token
        headers = {
            "Authorization": f"Bearer {oauth_token}"
        }
        params = {
            "max": 1,
            "keyword": city.upper()
        }
        response = requests.get(url=self.city_search_endpoint, headers=headers, params=params)
        response.raise_for_status()
        try:
            data = response.json()["data"][0]
        except IndexError:
            print(f"IndexError: No flights found for city: {city}")
            return "Not found"
        except KeyError:
            print(f"Key Error: No flights found for city: {city}")
            return "N/A"
        return data