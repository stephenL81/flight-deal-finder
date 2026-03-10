import os
from dotenv import load_dotenv
import requests

load_dotenv()

class FlightSearch:
    """This class is responsible for talking to the Flight Search API (Duffel)."""
    
    def __init__(self):
        self.duffel_token = os.getenv("DUFFEL_TOKEN")  # Load from .env
        self.duffel_iata_endpoint = "https://api.duffel.com/places/suggestions"
        self.duffel_flights_endpoint = "https://api.duffel.com/air/offer_requests"
    
    def get_iata_code(self, city_name):
        """Get IATA city code for a given city name."""
        params = {"query": city_name}
        headers = {
            "Authorization": f"Bearer {self.duffel_token}",
            "Duffel-Version": "v2"
        }
        
        response = requests.get(self.duffel_iata_endpoint, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        # Find the first city-type result
        for place in data["data"]:
            if place["type"] == "city":
                return place["iata_city_code"]
        
        return None
    
    def search_flights(self, origin_iata, destination_iata, outbound_date, return_date):
        """Search for round-trip flights between two cities."""
        headers = {
            "Authorization": f"Bearer {self.duffel_token}",
            "Duffel-Version": "v2",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        body = {
            "data": {
                "slices": [
                    {
                        "origin": origin_iata,
                        "destination": destination_iata,
                        "departure_date": outbound_date
                    },
                    {
                        "origin": destination_iata,
                        "destination": origin_iata,
                        "departure_date": return_date
                    }
                ],
                "passengers": [{"type": "adult"}],
                "cabin_class": "economy",
                "max_connections": 0
            }
        }
        
        # Create offer request
        response = requests.post(self.duffel_flights_endpoint, json=body, headers=headers)
        response.raise_for_status()
        json_response = response.json()
        offer_request_id = json_response["data"]["id"]
        
        # Get offers for the request
        offers_url = f"https://api.duffel.com/air/offers?offer_request_id={offer_request_id}"
        offers_response = requests.get(offers_url, headers=headers)
        offers_response.raise_for_status()
        
        return offers_response.json()
