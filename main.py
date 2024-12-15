#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
from data_manager import DataManager
from flight_search import FlightSearch
from datetime import datetime, timedelta
from flight_data import *
from notification_manager import NotificationManager

ORIGIN_CODE = "LON"

data_manager = DataManager()
sheet_data = data_manager.flight_sheet_data()
flight_manager = FlightSearch()
dept_date = datetime.now() + timedelta(days=1)
return_date = datetime.now() + timedelta(days=180)
sms_manager = NotificationManager()


for data in sheet_data:
    dest_code = data.get('iataCode')
    flight_data = flight_manager.flight_search(origin_code=ORIGIN_CODE, dest_code=dest_code, departure_date=dept_date,
                                    return_date=return_date, adults=1, nonStop="true", currencyCode="GBP", max=10)
    flight = find_cheapest_flight(flight_data)
    if flight.price != 'N/A' and flight.price < float(data.get('lowestPrice')):
        sms_manager.send_sms(subject="Lowest Price Alert",
                             body=f"Only £{flight.price} to fly from {flight.origin_airport} to "
                                  f"{flight.destination_airport}, on {flight.out_date} until {flight.return_date}")


