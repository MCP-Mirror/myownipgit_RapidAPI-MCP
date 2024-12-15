import requests
import json
from typing import Dict, Any
import os
from dotenv import load_dotenv

class RapidAPIPatentClient:
    def __init__(self):
        load_dotenv()
        self.base_url = "https://patentsearch.p.rapidapi.com"  # Updated URL
        self.api_key = os.getenv('RAPIDAPI_KEY')
        if not self.api_key:
            raise ValueError("RAPIDAPI_KEY not found in environment variables")
            
        self.headers = {
            "X-RapidAPI-Key": self.api_key,
            "X-RapidAPI-Host": "patentsearch.p.rapidapi.com",  # Updated host
            "Content-Type": "application/json"
        }
        
    def search_patents(self, query_params: Dict[str, Any]) -> Dict:
        """
        Search for patents using the RapidAPI endpoint
        """
        try:
            # Print request details for debugging
            print(f"Making request to: {self.base_url}/patents/search")
            print(f"Headers: {self.headers}")
            print(f"Query params: {query_params}")
            
            response = requests.get(
                f"{self.base_url}/patents/search",
                headers=self.headers,
                params=query_params
            )
            
            # Print response status and headers for debugging
            print(f"Response status: {response.status_code}")
            print(f"Response headers: {response.headers}")
            
            if response.status_code == 401:
                print("Authentication error - check your API key")
                return {}
                
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error during API request: {str(e)}")
            if hasattr(e.response, 'text'):
                print(f"Response text: {e.response.text}")
            return {}

    def get_patent_details(self, patent_number: str) -> Dict:
        """
        Get detailed information for a specific patent
        """
        try:
            response = requests.get(
                f"{self.base_url}/patents/{patent_number}",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching patent details: {str(e)}")
            return {}