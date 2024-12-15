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
                                    "_text_phrase": {
                                        "patent_title": "quantum computing"
                                    }
                                },
                                {
                                    "_and": [
                                        {
                                            "_text_all": {
                                                "patent_abstract": ["quantum", "computing"]
                                            }
                                        },
                                        {
                                            "_or": [
                                                {"cpc_group_id": "G06N-010"}, # Quantum computing
                                                {"cpc_group_id": "G06N-99"}, # Subject matter not provided for in other groups
                                                {"cpc_group_id": "H01L-039"} # Superconducting devices
                                            ]
                                        }
                                    ]
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
                    "inventor_last_name",
                    "inventor_first_name",
                    "cpc_group_id",
                    "cpc_group_title",
                    "cpc_section_id",
                    "cpc_subsection_id"
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
                'total_patent_count': result.get('total_patent_count', 0),
                'patents': [{
                    'patentNumber': patent.get('patent_number'),
                    'title': patent.get('patent_title'),
                    'date': patent.get('patent_date'),
                    'type': patent.get('patent_type'),
                    'abstract': patent.get('patent_abstract'),
                    'assignee': patent.get('assignee_organization'),
                    'processingTime': patent.get('patent_processing_time'),
                    'kind': patent.get('patent_kind'),
                    'inventor': f"{patent.get('inventor_first_name', '')} {patent.get('inventor_last_name', '')}".strip(),
                    'cpcGroup': f"{patent.get('cpc_group_id', '')} - {patent.get('cpc_group_title', '')}",
                    'cpcSection': patent.get('cpc_section_id', ''),
                    'cpcSubsection': patent.get('cpc_subsection_id', '')
                } for patent in result.get('patents', [])]
            }
            
        except requests.exceptions.RequestException as e:
            print(f"Error during API request: {str(e)}")
            if hasattr(e, 'response') and hasattr(e.response, 'text'):
                print(f"Response text: {e.response.text}")
            return {}