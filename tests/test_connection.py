import asyncio
from patent_mcp.client import RapidAPIPatentClient

async def test_api_connection():
    client = RapidAPIPatentClient()
    
    # Test simple search
    test_query = {
        'query': 'quantum computing',
        'date_range': '2023-2024',
        'page': 1,
        'per_page': 5
    }
    
    print('Testing API connection...')
    try:
        results = client.search_patents(test_query)
        if results:
            print('✓ Connection successful!')
            print(f'Found {len(results.get("patents", []))} patents')
            print('\nSample result:')
            if results.get('patents'):
                patent = results['patents'][0]
                print(f'Title: {patent.get("title")}')
                print(f'Document Number: {patent.get("publication_number")}')
        else:
            print('✗ No results returned')
    except Exception as e:
        print(f'✗ Connection failed: {str(e)}')

if __name__ == '__main__':
    asyncio.run(test_api_connection())
