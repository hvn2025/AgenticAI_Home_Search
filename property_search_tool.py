from crewai.tools import BaseTool
from pydantic import BaseModel, Field
import requests
import os
class PropertySearchTool(BaseTool):
    """
    A tool to search for real estate properties for sale using the RentCast API.
    This tool supports searching by address, city, state, zip code, or geographic
    coordinates (latitude, longitude, radius), along with optional criteria
    like bedrooms, bathrooms, and property type.
    """
    name: str = "Property Sale Listings Search Tool"
    description: str = (
        "Searches for real estate properties FOR SALE. Can search by: "
        "1. Full address (Street, City, State, Zip). "
        "2. City, State, or Zip Code. "
        "3. Geographic coordinates (latitude, longitude, radius in miles). "
        "Also accepts optional criteria like min/max price, beds, baths, and property type. "
        "Returns a list of properties for sale."
    )

    def _run(self, **kwargs) -> str:
        """
        Executes the property search for sale listings using the RentCast API.

        Prioritizes location parameters in this order:
        1. address, city, state, zip_code (if provided)
        2. latitude, longitude, radius (if provided)
        3. Default Austin, TX coordinates (if no location is provided by LLM)

        Optional kwargs (case-insensitive and flexible to natural language):
        - address (str, optional): Full address of the property.
        - city (str, optional): City for property search.
        - state (str, optional): 2-character state abbreviation (e.g., 'TX').
        - zip_code (str, optional): 5-digit zip code.
        - latitude (float, optional): Latitude of the center point for the search.
        - longitude (float, optional): Longitude of the center point for the search.
        - radius (int, optional): Search radius in miles.
        - min_price (int, optional): Minimum price for the property.
        - max_price (int, optional): Maximum price for the property.
        - beds (int, optional): Number of bedrooms.
        - baths (int, optional): Number of bathrooms.
        - property_type (str, optional): Type of property (e.g., 'single_family', 'condo').
        """
        RENTCAST_API_KEY = os.getenv("RENTCAST_API_KEY")
        if not RENTCAST_API_KEY:
            return "Error: RentCast API key not found. Please set it in your .env file."

        url = "https://api.rentcast.io/v1/listings/sale"

        headers = {
            "accept": "application/json",
            "X-Api-Key": RENTCAST_API_KEY
        }

        params = {'limit': 10} # Default limit, can be made configurable if needed

        # --- Location Parameter Handling Logic ---
        # Prioritize text-based location
        if 'address' in kwargs:
            params['address'] = kwargs['address']
        elif 'city' in kwargs and 'state' in kwargs:
            params['city'] = kwargs['city']
            params['state'] = kwargs['state']
            if 'zip_code' in kwargs: # Optional zip code with city/state
                params['zipCode'] = kwargs['zip_code']
        elif 'zip_code' in kwargs: # Search by zip code alone
            params['zipCode'] = kwargs['zip_code']
        # Fallback to geographic coordinates if no text-based location provided
        elif 'latitude' in kwargs and 'longitude' in kwargs and 'radius' in kwargs:
            params['latitude'] = kwargs['latitude']
            params['longitude'] = kwargs['longitude']
            params['radius'] = kwargs['radius']
        else:
            # --- PROTOTYPE ADJUSTMENT: Use default coordinates if no location is provided by LLM ---
            # For a real application, you would use a geocoding API here or require user input
            params['latitude'] = 30.2672   # Default to Austin, TX latitude
            params['longitude'] = -97.7431 # Default to Austin, TX longitude
            params['radius'] = 5           # Default to 5-mile radius
            print("Note: No specific location provided by LLM. Using default Austin, TX coordinates for search.")


        # Add other optional criteria
        if 'min_price' in kwargs:
            params['minPrice'] = kwargs['min_price']
        if 'max_price' in kwargs:
            params['maxPrice'] = kwargs['max_price']
        if 'beds' in kwargs:
            params['bedrooms'] = kwargs['beds'] # RentCast uses 'bedrooms' for sale listings
        if 'baths' in kwargs:
            params['bathrooms'] = kwargs['baths'] # RentCast uses 'bathrooms' for sale listings
        if 'property_type' in kwargs:
            params['propertyType'] = kwargs['property_type']
        if 'status' in kwargs: # Added status parameter for more refined search
            params['status'] = kwargs['status']


        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
            properties = response.json()

            if not properties:
                # Provide more context if using default location
                if 'latitude' not in kwargs and 'longitude' not in kwargs and 'radius' not in kwargs \
                   and 'address' not in kwargs and 'city' not in kwargs and 'state' not in kwargs and 'zip_code' not in kwargs:
                    return "No properties found matching your criteria using default Austin, TX location. Try a more specific query or different criteria."
                else:
                    return "No properties found matching your criteria."

            # Format the results into a human-readable string
            formatted_results = "Found the following properties for sale:\n"
            for i, prop in enumerate(properties[:3]): # Limit to first 3 for brevity
                formatted_results += f"--- Property {i+1} ---\n"
                formatted_results += f"Address: {prop.get('formattedAddress', 'N/A')}\n"
                formatted_results += f"Price: ${prop.get('price', 'N/A'):,.0f}\n"
                formatted_results += f"Beds: {prop.get('bedrooms', 'N/A')}, Baths: {prop.get('bathrooms', 'N/A')}\n"
                formatted_results += f"Type: {prop.get('propertyType', 'N/A')}\n"
                formatted_results += f"Status: {prop.get('status', 'N/A')}\n"
                formatted_results += f"Days on Market: {prop.get('daysOnMarket', 'N/A')}\n" # Added Days on Market
                # Add more details as needed from the RentCast API response structure for listings/sale
            return formatted_results

        except requests.exceptions.HTTPError as errh:
            return f"HTTP Error: {errh} - {errh.response.text if errh.response is not None else 'Unknown error'}. Check API key or request parameters."
        except requests.exceptions.ConnectionError as errc:
            return f"Error Connecting: {errc} - Check your internet connection."
        except requests.exceptions.Timeout as errt:
            return f"Timeout Error: {errt} - Request took too long."
        except requests.exceptions.RequestException as err:
            return f"An unexpected error occurred: {err}"
        except Exception as e:
            return f"An error occurred while processing the RentCast API response: {e}"