import os
from dotenv import load_dotenv
import requests
from flight_search import FlightSearch

load_dotenv()

class DataManager:
    """This class is responsible for talking to the Google Sheet via Sheety API."""
    
    def __init__(self):
        self.sheety_endpoint = os.getenv("SHEETY_ENDPOINT")  # Load from .env
        self.sheety_token = os.getenv("SHEETY_TOKEN")  # Load from .env
        self.sheety_headers = {
            "Authorization": f"Bearer {self.sheety_token}",
        }
    
    def get_destination_data(self):
        """Get all destination data from the Google Sheet."""
        response = requests.get(self.sheety_endpoint, headers=self.sheety_headers)
        response.raise_for_status()
        data = response.json()
        return data["prices"]
    
    def set_missing_iatas(self):
        """Populate missing IATA codes in the spreadsheet."""
        flight_search = FlightSearch()
        rows = self.get_destination_data()
        
        for row in rows:
            if row["iataCode"] == "":
                city_name = row["city"]
                iata_code = flight_search.get_iata_code(city_name)
                
                if iata_code:
                    row_id = row["id"]
                    update_url = f"{self.sheety_endpoint}/{row_id}"
                    
                    body = {
                        "price": {
                            "iataCode": iata_code
                        }
                    }
                    
                    update_response = requests.put(update_url, json=body, headers=self.sheety_headers)
                    update_response.raise_for_status()
                    print(f"Updated {city_name} with code {iata_code}")
                else:
                    print(f"Could not find IATA code for {city_name}")
