# This file orchestrates the DataManager, FlightSearch, FlightData, and NotificationManager classes
from data_manager import DataManager
from notification_manager import NotificationManager

# Main execution
if __name__ == "__main__":
    # Step 1: Get destination data from Google Sheet
    data_manager = DataManager()
    
    # Uncomment this line on first run to populate IATA codes in the sheet
    # data_manager.set_missing_iatas()
    
    # Step 2: Get flight deals and send notifications
    notification_manager = NotificationManager()
    notification_manager.send_flight_deals()
    
    print("Flight deal search complete!")