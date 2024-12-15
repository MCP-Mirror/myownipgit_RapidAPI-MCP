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
    
    print('\nTesting PatentsView API connection...')
    try:
        results = client.search_patents(test_query)
        if results and results.get('patents'):
            print('✅ Connection successful!')
            print(f'Found {len(results["patents"])} patents')
            print('\nSample results:')
            for patent in results['patents']:
                print(f'\n{"="*80}')
                print(f'Title: {patent.get("title")}')
                print(f'Patent Number: {patent.get("patentNumber")}')
                print(f'Date: {patent.get("date")}')
                print(f'Type: {patent.get("type")}')
                print(f'Kind: {patent.get("kind")}')
                print(f'Assignee: {patent.get("assignee")}')
                print(f'Inventor: {patent.get("inventor")}')
                print(f'CPC Group: {patent.get("cpcGroup")}')
                if patent.get('abstract'):
                    print(f'Abstract: {patent.get("abstract")[:200]}...')
        else:
            print('❌ No results returned')
    except Exception as e:
        print(f'❌ Error: {str(e)}')

if __name__ == '__main__':
    asyncio.run(test_api_connection())