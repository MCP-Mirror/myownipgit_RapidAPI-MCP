import requests
import json
from typing import Dict, Any
import os
from dotenv import load_dotenv

class PatentAPIClient:
    def __init__(self):
        load_dotenv()
        self.base_url = "https://api.patentsview.org/patents"
        
    def search_patents(self, query_params: Dict[str, Any]) -> Dict:
        """
        Search for patents using the PatentsView API
        """
        try:
            # Convert query params to PatentsView format
            search_criteria = {
                "q": {
                    "_and": [
                        {
                            "_or": [
                                {
                                    "_text_all": {
                                        "patent_title": query_params['searchText'].split()
                                    }
                                },
                                {
                                    "_text_all": {
                                        "patent_abstract": query_params['searchText'].split()
                                    }
                                }
                            ]
                        },
                        {
                            "_gte": {
                                "patent_date": query_params['start']
                            }
                        },
                        {
                            "_lte": {
                                "patent_date": query_params['end']
                            }
                        }
                    ]
                },
                "f": [
                    "patent_number", 
                    "patent_title", 
                    "patent_date", 
                    "patent_type", 
                    "patent_abstract",
                    "assignee_organization",
                    "patent_processing_time",
                    "patent_kind",
                    "inventors",
                    "cpc_codes"
                ],
                "o": {
                    "page": query_params['pageNumber'], 
                    "per_page": query_params['pageSize'],
                    "sort": ["patent_date desc"]
                }
            }
            
            # Print request details for debugging
            print(f"Making request to: {self.base_url}/query")
            print(f"Query params: {json.dumps(search_criteria, indent=2)}")
            
            response = requests.post(
                f"{self.base_url}/query",
                json=search_criteria,
                headers={'Content-Type': 'application/json'}
            )
            
            # Print response status and headers for debugging
            print(f"Response status: {response.status_code}")
            if response.status_code != 200:
                print(f"Response text: {response.text}")
            
            response.raise_for_status()
            result = response.json()
            
            # Transform response to match expected format
            return {
                'patents': [{
                    'patentNumber': patent.get('patent_number'),
                    'title': patent.get('patent_title'),
                    'date': patent.get('patent_date'),
                    'type': patent.get('patent_type'),
                    'abstract': patent.get('patent_abstract'),
                    'assignee': patent.get('assignee_organization'),
                    'processingTime': patent.get('patent_processing_time'),
                    'kind': patent.get('patent_kind'),
                    'inventors': patent.get('inventors'),
                    'cpcCodes': patent.get('cpc_codes')
                } for patent in result.get('patents', [])]
            }
            
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
            search_criteria = {
                "q": {"patent_number": patent_number},
                "f": ["*"]
            }
            
            response = requests.post(
                f"{self.base_url}/query",
                json=search_criteria,
                headers={'Content-Type': 'application/json'}
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching patent details: {str(e)}")
            return {}