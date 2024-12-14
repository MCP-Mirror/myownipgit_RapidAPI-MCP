from .client import RapidAPIPatentClient
from .database import PatentDatabase
from typing import Dict, Any
import asyncio

class MCPPatentServer:
    def __init__(self):
        self.api_client = RapidAPIPatentClient()
        self.db = PatentDatabase()
        
    async def handle_patent_request(self, request_data: Dict[str, Any]) -> Dict:
        """
        Handle incoming MCP requests and route to appropriate API endpoints
        """
        command = request_data.get('command')
        if command == 'search':
            return await self.search_patents(request_data.get('params', {}))
        elif command == 'details':
            return await self.get_patent_details(request_data.get('patent_number'))
        else:
            return {'error': 'Invalid command'}

    async def search_patents(self, search_params: Dict[str, Any]) -> Dict:
        """
        Search patents and format response for SQLite storage
        """
        results = self.api_client.search_patents(search_params)
        formatted_results = self.format_for_sqlite(results)
        await self.db.store_patents(formatted_results)
        return formatted_results

    def format_for_sqlite(self, api_results: Dict) -> list:
        """
        Format API results to match SQLite schema
        """
        formatted_data = []
        for result in api_results.get('patents', []):
            formatted_record = {
                'document_no': result.get('publication_number'),
                'title': result.get('title'),
                'country_code': result.get('country_code'),
                'current_assignee': result.get('assignee'),
                'document_status': result.get('status'),
                'application_status': result.get('app_status'),
                'cpc_first': result.get('cpc_main'),
                'cpc_inventive': result.get('cpc_further'),
                'file_date': result.get('filing_date'),
                'grant_date': result.get('grant_date'),
                'pscore': 0,
                'cscore': 0,
                'lscore': 0,
                'tscore': 0,
                'prior_art_score': 0,
                'pendency': self.calculate_pendency(result),
                'category': self.determine_category(result)
            }
            formatted_data.append(formatted_record)
        return formatted_data

    def calculate_pendency(self, patent_data: Dict) -> int:
        """
        Calculate pendency in days between filing and grant dates
        """
        # Implementation needed
        return 0

    def determine_category(self, patent_data: Dict) -> str:
        """
        Determine patent category based on CPC codes
        """
        # Implementation needed
        return 'UNKNOWN'