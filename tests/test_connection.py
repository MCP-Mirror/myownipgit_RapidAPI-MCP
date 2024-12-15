import asyncio
from patent_mcp.client import RapidAPIPatentClient
import os
from dotenv import load_dotenv

async def test_api_connection():
    # Ensure environment variables are loaded
    load_dotenv()
    
    # Verify API key is present
    api_key = os.getenv('RAPIDAPI_KEY')
    if not api_key:
        print('❌ Error: RAPIDAPI_KEY not found in environment variables')
        return
        
    print(f'Using API key: {api_key[:8]}...')
    
    client = RapidAPIPatentClient()
    
    # Test simple search
    test_query = {
        'q': 'quantum computing',  # Updated parameter name
        'from': '2023',           # Updated date parameter
        'to': '2024',             # Updated date parameter
        'page': 1,
        'limit': 5                # Updated parameter name
    }
    
    print('\nTesting API connection...')
    try:
        results = client.search_patents(test_query)
        if results:
            print('✅ Connection successful!')
            print(f'Found {len(results.get("patents", []))} patents')
            print('\nSample result:')
            if results.get('patents'):
                patent = results['patents'][0]
                print(f'Title: {patent.get("title")}')
                print(f'Document Number: {patent.get("publication_number")}')
        else:
            print('❌ No results returned')
    except Exception as e:
        print(f'❌ Error: {str(e)}')

if __name__ == '__main__':
    asyncio.run(test_api_connection())