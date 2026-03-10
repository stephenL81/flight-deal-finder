Day 39 - Flight Deal Finder App (Capstone Project)

Description:
This is a last-minute flight deal finder that monitors round-trip flight prices from London to multiple destinations and sends SMS alerts when prices fall below a specified budget. The app automatically searches for flights departing within the next 7 days, compares prices against user-defined maximum budgets stored in a Google Sheet, and sends text notifications via Twilio when deals are found. This project demonstrates API integration, data management, object-oriented programming, and automated notification systems.

The app was adapted from the original course specifications due to API availability changes (see "Project Adaptations" below).



How to Run:

1. Install required dependencies:
   pip install requests twilio python-dotenv

2. Set up API accounts:
   - Duffel (for flight data): https://duffel.com (free tier: 800 requests/day)
   - Sheety (for Google Sheets API): https://sheety.co (free)
   - Twilio (for SMS): https://www.twilio.com (trial account works)

3. Set up your Google Sheet:
   - Create a Google Sheet with columns: city, iataCode, lowestPrice, numberOfDays
   - Fill in cities you want to monitor, your maximum price for each, and desired trip length in days
   - Leave iataCode empty initially (the app will populate these automatically)
   - Share the sheet so "Anyone with the link" can edit
   - Connect the sheet to Sheety and copy the endpoint URL

4. Configure environment variables:
   - Copy .env.example to .env
   - Fill in all your API credentials:
     * DUFFEL_TOKEN (from Duffel dashboard)
     * SHEETY_ENDPOINT (your Sheety API URL)
     * SHEETY_TOKEN (Bearer token from Sheety)
     * TWILIO_ACCOUNT_SID (from Twilio console)
     * TWILIO_AUTH_TOKEN (from Twilio console)
     * TWILIO_FROM_NUMBER (your Twilio phone number, format: +44xxxxxxxxxx)
     * TWILIO_TO_NUMBER (your personal phone number, format: +44xxxxxxxxxx)

5. First run - populate IATA codes:
   Uncomment the line in main.py:
   `# data_manager.set_missing_iatas()`
   Run once, then comment it out again.

6. Run the app:
   python main.py



How It Works (Code Overview):

main.py → Orchestrates all classes to execute the flight deal search workflow:
- Coordinates DataManager, FlightSearch, FlightData, and NotificationManager classes
- Provides a clean entry point for running the entire application


flight_search.py → Handles all communication with the Duffel Flight API:
- get_iata_code(): Searches for and returns IATA city codes for destination cities
- search_flights(): Makes API requests to find round-trip flights for specific date combinations
- Returns flight offer data including prices, dates, and flight details


data_manager.py → Manages Google Sheets data via the Sheety API:
- get_destination_data(): Retrieves the list of destinations with max prices and trip durations from the spreadsheet
- set_missing_iatas(): Automatically populates missing IATA codes in the spreadsheet using the FlightSearch class
- Handles all API communication with Sheety including PUT requests to update sheet data


flight_data.py → Contains the core logic for finding and filtering flight deals:
- get_date_range(): Generates a list of dates for the next 7-14 days to check for flights
- find_deals(): Searches all destinations across all dates, filters results by maximum price, and returns only deals under budget
- Structures the deal data into a clean format for notification sending
- Implements error handling for API request failures


notification_manager.py → Sends SMS notifications for flight deals via Twilio:
- send_flight_deals(): Coordinates the deal-finding process and sends formatted SMS messages for each deal found
- Formats messages to include origin, destination, departure date, return date, and price
- Includes error handling for failed message sends


Environment Variables (dotenv) → Securely stores all API credentials:
- All sensitive information (API keys, tokens, phone numbers) is stored in a .env file
- The .env file is excluded from version control via .gitignore
- Credentials are loaded at runtime using python-dotenv



Key Features:
- Automated flight price monitoring: Checks multiple destinations across a range of dates
- Budget-aware filtering: Only alerts on flights under your specified maximum price
- SMS notifications: Sends text alerts directly to your phone via Twilio
- Google Sheets integration: Easy-to-manage destination and budget configuration
- Non-stop flights only: Filters for direct flights to minimize travel time
- Round-trip search: Searches complete round-trip journeys with customizable trip durations
- Object-oriented design: Clean separation of concerns across multiple classes
- Environment variable security: API credentials safely stored and never committed to version control



Project Adaptations:
This project required significant adaptation from the original course specifications due to third-party API changes:


Challenge 1 - API Provider Change:
The original project specified using the Amadeus Flight API, which discontinued free tier access for new users during development. The Amadeus API offered a specialized "Inspiration Search" endpoint that could search across flexible date ranges and return the cheapest destinations within a budget - a feature designed specifically for this type of flight deal finder.

Solution: Migrated to the Duffel Flight API, which offers a more generous free tier (800 requests/day vs Amadeus's 25/day limit for those with access). However, Duffel does not offer an inspiration search endpoint and requires specific departure and return dates for each request.


Challenge 2 - Search Methodology Redesign:
The original specification called for searching flights up to 6 months in advance across all possible destinations and date combinations. With Duffel requiring individual requests for each date combination, this approach would have required hundreds of API calls per search (180 days × 3 destinations = 540+ requests), quickly exhausting the free tier and making the app impractical for regular use.

Solution: Reframed the project as a "Last-Minute Flight Deals" finder focusing on the next 2 weeks rather than 6 months. This is actually a more realistic use case - travelers booking spontaneous trips typically look 1-2 weeks ahead rather than months in advance. The reduced timeframe (14 days × 3 destinations = 42 requests) makes the app sustainable within free tier limits while still providing genuine value.


Challenge 3 - Date Range Implementation:
Without a native date range search feature in Duffel, the app needed to programmatically generate and test multiple date combinations.

Solution: Implemented a date generation utility that creates a range of departure dates, calculates corresponding return dates based on user-specified trip durations, and systematically checks each combination. This provides flexibility while keeping API usage reasonable.


Challenge 4 - SMS Character Limits:
Twilio trial accounts impose a strict 160-character limit per message, and the initial implementation tried to send comprehensive flight details that exceeded this limit.

Solution: Redesigned the message format to be concise but informative, sending one message per deal with essential information only (route, dates, price). The formatted messages prioritize clarity while respecting the character constraint.



Technical Skills Demonstrated:
- API Integration: Successfully integrated three different APIs (Duffel, Sheety, Twilio) with different authentication methods
- Problem-Solving: Adapted project requirements when facing real-world API limitations
- Object-Oriented Programming: Implemented clean OOP design with proper separation of concerns
- Data Management: Automated data retrieval and updates between Google Sheets and flight search APIs
- Error Handling: Implemented try-except blocks and API response validation
- Environment Security: Properly secured API credentials using environment variables
- Product Thinking: Reframed project scope to create a more practical, sustainable application



Notes:
- The app searches for direct (non-stop) flights only to ensure quick journeys
- London (LON) is hardcoded as the origin city as this is a UK-based personal project
- Trip duration is customizable per destination via the Google Sheet
- Twilio trial accounts have SMS limits - consider upgrading for production use
- The app can be easily modified to support different origin cities or additional destinations
- Free tier API limits make this suitable for personal use; production deployment would require paid tiers
