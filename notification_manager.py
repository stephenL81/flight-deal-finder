import os
from dotenv import load_dotenv
from twilio.rest import Client
from flight_data import FlightData
from datetime import datetime

load_dotenv()

class NotificationManager:
    """This class is responsible for sending SMS notifications with flight deal details."""
    
    def __init__(self):
        self.TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")  # Load from .env
        self.TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")  # Load from .env
        self.FROM_NUMBER = os.getenv("TWILIO_FROM_NUMBER")  # Load from .env
        self.TO_NUMBER = os.getenv("TWILIO_TO_NUMBER")  # Load from .env
    
    def send_flight_deals(self):
        """Find flight deals and send SMS notifications for each one."""
        # Get flight deals
        flight_data = FlightData()
        deals = flight_data.find_deals()
        
        if not deals:
            print("No deals found within budget.")
            return
        
        # Send SMS for each deal
        client = Client(self.TWILIO_ACCOUNT_SID, self.TWILIO_AUTH_TOKEN)
        
        for deal in deals:

            outbound_formatted = datetime.strptime(deal['outbound_date'], "%Y-%m-%d").strftime("%d-%b-%Y")
            return_formatted = datetime.strptime(deal['return_date'], "%Y-%m-%d").strftime("%d-%b-%Y")

            message_body = (
                f"{deal['origin']} → {deal['destination']}\\n"
                f"Depart: {outbound_formatted}\\n"
                f"Return: {return_formatted}\\n"
                f"Price: £{deal['price']:.2f}"
            )

            try:
                message = client.messages.create(
                    body=message_body,
                    from_=self.FROM_NUMBER,
                    to=self.TO_NUMBER
                )
                print(f"✓ SMS sent successfully (SID: {message.sid})")
                print(f"  Deal: {deal['destination']} for £{deal['price']:.2f}\n")
            
            except Exception as e:
                print(f"✗ Failed to send SMS for {deal['destination']}: {e}\n")
