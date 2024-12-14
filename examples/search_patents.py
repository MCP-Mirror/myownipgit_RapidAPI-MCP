import asyncio
from patent_mcp.server import MCPPatentServer

async def main():
    # Initialize the MCP Server
    server = MCPPatentServer()

    # Example search request
    search_request = {
        'command': 'search',
        'params': {
            'query': 'quantum computing',
            'date_range': '2004-2024',
            'page': 1,
            'per_page': 100
        }
    }

    # Execute search
    results = await server.handle_patent_request(search_request)

    # Print results
    print(f"Found {len(results)} patents")
    for patent in results[:5]:  # Print first 5 results
        print(f"\nPatent: {patent['document_no']}")
        print(f"Title: {patent['title']}")
        print(f"Scores: P={patent['pscore']:.2f}, C={patent['cscore']:.2f}, "  \
              f"L={patent['lscore']:.2f}, T={patent['tscore']:.2f}")

if __name__ == '__main__':
    asyncio.run(main())