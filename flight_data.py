class FlightData:
    #This class is responsible for structuring the flight data.
    def __init__(self, price, origin_airport, destination_airport, out_date, return_date):
        self.price = price
        self.origin_airport = origin_airport
        self.destination_airport = destination_airport
        self.out_date = out_date
        self.return_date = return_date


def find_cheapest_flight(data):
    if data is None or not data['data']:
        print("No Flights are available")
        return FlightData(price="N/A", origin_airport="N/A", destination_airport="N/A",
                          out_date="N/A",return_date="N/A")
    flights = data['data']
    ff_data = flights[0]
    price = float(ff_data['price']['total'])
    origin = ff_data['itineraries'][0]['segments'][0]['departure']['iataCode']
    destination = ff_data['itineraries'][0]['segments'][0]['arrival']['iataCode']
    out_date = ff_data['itineraries'][0]['segments'][0]['departure']['at'].split('T')[0]
    return_date = ff_data['itineraries'][1]['segments'][0]['departure']['at'].split('T')[0]

    cheap_flight = FlightData(price=price, origin_airport=origin, destination_airport=destination,
                              out_date=out_date, return_date=return_date)
    best_price = cheap_flight.price
    for flight in flights:
        if best_price > float(flight['price']['total']):
            price = float(flight['price']['total'])
            origin = flight['itineraries'][0]['segments'][0]['departure']['iataCode']
            destination = flight['itineraries'][0]['segments'][0]['arrival']['iataCode']
            out_date = flight['itineraries'][0]['segments'][0]['departure']['at'].split('T')[0]
            return_date = flight['itineraries'][1]['segments'][0]['departure']['at'].split('T')[0]
            cheap_flight = FlightData(price=price, origin_airport=origin, destination_airport=destination,
                                      out_date=out_date, return_date=return_date)
        best_price = float(flight['price']['total'])
    return cheap_flight