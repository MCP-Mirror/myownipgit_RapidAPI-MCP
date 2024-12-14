# RapidAPI MCP Server

This repository contains an implementation of an MCP Server for interfacing with the RapidAPI Global Patent API and storing patent data in a SQLite database.

## Features

- RapidAPI Global Patent API integration
- MCP Server implementation for handling patent requests
- SQLite database integration for patent data storage
- Custom patent scoring system
- Rate limiting and error handling

## Installation

1. Clone the repository:
```bash
git clone https://github.com/myownipgit/RapidAPI-MCP.git
cd RapidAPI-MCP
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
export RAPIDAPI_KEY="your_api_key"
```

## Usage

1. Initialize the MCP Server:
```python
from patent_mcp.server import MCPPatentServer

mcp_server = MCPPatentServer()
```

2. Handle patent search requests:
```python
search_request = {
    'command': 'search',
    'params': {
        'query': 'quantum computing',
        'date_range': '2004-2024',
        'page': 1,
        'per_page': 100
    }
}

results = await mcp_server.handle_patent_request(search_request)
```

## Project Structure

- `patent_mcp/` - Main package directory
  - `client.py` - RapidAPI client implementation
  - `server.py` - MCP Server implementation
  - `database.py` - SQLite database operations
  - `utils.py` - Utility functions and helpers

## Configuration

The server uses the following environment variables:
- `RAPIDAPI_KEY`: Your RapidAPI API key
- `DB_PATH`: Path to SQLite database (optional, defaults to `./patents.db`)

## License

MIT License - see LICENSE file for details