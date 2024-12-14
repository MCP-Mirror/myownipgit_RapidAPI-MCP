import requests
import json
from typing import Dict, Any

class RapidAPIPatentClient:
    def __init__(self):
        self.base_url = "https://patent-search.p.rapidapi.com"
        self.headers = {
            "X-RapidAPI-Key": "6b42cccca1msh4a3e18dd576531dp10f357jsnd96f0670947d",
            "X-RapidAPI-Host": "patent-search.p.rapidapi.com",
            "Content-Type": "application/json"
        }

    def search_patents(self, query_params: Dict[str, Any]) -> Dict:
        """
        Search for patents using the RapidAPI endpoint
        """
        try:
            response = requests.get(
                f"{self.base_url}/search",
                headers=self.headers,
                params=query_params
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error during API request: {str(e)}")
            return {}

    def get_patent_details(self, patent_number: str) -> Dict:
        """
        Get detailed information for a specific patent
        """
        try:
            response = requests.get(
                f"{self.base_url}/patent/{patent_number}",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching patent details: {str(e)}")
            return {}