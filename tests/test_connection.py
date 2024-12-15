import asyncio
from patent_mcp.client import PatentAPIClient

async def test_api_connection():
    client = PatentAPIClient()
    
    # Test simple search
    test_query = {
        'searchText': 'quantum computing',
        'start': '2023-01-01',
        'end': '2024-12-31',
        'pageSize': 5,
        'pageNumber': 1
    }
    
    print('\nTesting USPTO API connection...')
    try:
        results = client.search_patents(test_query)
        if results:
            print('✅ Connection successful!')
            print(f'Found {len(results.get("patents", []))} patents')
            print('\nSample result:')
            if results.get('patents'):
                patent = results['patents'][0]
                print(f'Title: {patent.get("title")}')
                print(f'Document Number: {patent.get("patentNumber")}')
        else:
            print('❌ No results returned')
    except Exception as e:
        print(f'❌ Error: {str(e)}')

if __name__ == '__main__':
    asyncio.run(test_api_connection())