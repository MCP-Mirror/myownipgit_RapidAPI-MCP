import requests
import json
from typing import Dict, Any
import os
from dotenv import load_dotenv

class PatentAPIClient:
    def __init__(self):
        load_dotenv()
        self.base_url = "https://developer.uspto.gov/ibd-api/v1"
        
    def search_patents(self, query_params: Dict[str, Any]) -> Dict:
        """
        Search for patents using the USPTO API
        """
        try:
            # Print request details for debugging
            print(f"Making request to: {self.base_url}/patent/search")
            print(f"Query params: {query_params}")
            
            response = requests.get(
                f"{self.base_url}/patent/search",
                params=query_params
            )
            
            # Print response status and headers for debugging
            print(f"Response status: {response.status_code}")
            print(f"Response headers: {response.headers}")
            
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error during API request: {str(e)}")
            if hasattr(e, 'response') and hasattr(e.response, 'text'):
                print(f"Response text: {e.response.text}")
            return {}

    def get_patent_details(self, patent_number: str) -> Dict:
        """
        Get detailed information for a specific patent
        """
        try:
            response = requests.get(
                f"{self.base_url}/patent/{patent_number}"
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching patent details: {str(e)}")
            return {}