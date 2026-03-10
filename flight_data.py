from datetime import date, timedelta
from flight_search import FlightSearch
from data_manager import DataManager


class FlightData:
    """This class is responsible for structuring and filtering flight data."""
    
    def __init__(self):
        self.origin_city_iata = "LON"  # Default origin (London)
    
    @staticmethod
    def get_date_range(num_days=7):
        """Generate a list of dates starting from tomorrow for the specified number of days."""
        date_range = []
        for i in range(num_days):
            next_date = date.today() + timedelta(days=i + 1)
            date_range.append(next_date)
        return date_range
    
    def find_deals(self):
        """Search for flight deals and return only those under the maximum price."""
        deals = []
        
        # Get destination data from spreadsheet
        data_manager = DataManager()
        destinations = data_manager.get_destination_data()
        
        # Get flight search API
        flight_search = FlightSearch()
        
        # Check each destination
        for destination in destinations:
            destination_iata = destination["iataCode"]
            max_price = destination["lowestPrice"]
            trip_duration = destination["numberOfDays"]
            city_name = destination["city"]
            
            # Check flights for each departure date
            dates = self.get_date_range()
            for departure_date in dates:
                # Calculate return date
                return_date = departure_date + timedelta(days=trip_duration)
                
                # Convert dates to strings
                departure_str = departure_date.strftime("%Y-%m-%d")
                return_str = return_date.strftime("%Y-%m-%d")
                
                try:
                    # Search for flights
                    flight_results = flight_search.search_flights(
                        origin_iata=self.origin_city_iata,
                        destination_iata=destination_iata,
                        outbound_date=departure_str,
                        return_date=return_str
                    )
                    
                    # Get the cheapest offer
                    if flight_results['data']:
                        cheapest_offer = flight_results['data'][0]
                        price = float(cheapest_offer['total_amount'])
                        
                        # Check if it's under budget
                        if price <= max_price:
                            deals.append({
                                'destination': city_name,
                                'origin': 'London',
                                'outbound_date': departure_str,
                                'return_date': return_str,
                                'price': price,
                                'max_price': max_price
                            })
                            print(f"Deal found: {city_name} for £{price}")
                
                except Exception as e:
                    print(f"Error searching flights to {city_name} on {departure_str}: {e}")
        
        return deals
