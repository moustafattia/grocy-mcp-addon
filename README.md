# Grocy MCP Add-on for Home Assistant

Home Assistant add-on that runs [grocy-mcp](https://github.com/moustafattia/grocy-mcp) as a persistent HTTP MCP server, enabling Claude.ai and other AI agents to manage your Grocy instance remotely.

## Features

- 30 Grocy tools: stock, shopping lists, recipes, chores, system management
- Stateless HTTP MCP transport for Claude.ai compatibility
- Auto-generated secret URL path (128-bit entropy) for security
- Two-stage Docker build for minimal image size

## Installation

1. In Home Assistant, go to **Settings > Add-ons > Add-on Store**
2. Click the overflow menu (top right) > **Repositories**
3. Add: `https://github.com/moustafattia/grocy-mcp-addon`
4. Find **Grocy MCP Server** in the store and install it

## Configuration

| Option | Required | Default | Description |
|--------|----------|---------|-------------|
| `grocy_url` | Yes | `http://homeassistant.local:9192` | URL of your Grocy instance |
| `grocy_api_key` | Yes | | API key from Grocy (Settings > Manage API keys) |
| `port` | No | `9193` | HTTP port for the MCP server |
| `secret_path` | No | auto-generated | Custom secret URL path |

## Usage with Claude.ai

1. Start the add-on and check the logs for the MCP endpoint URL
2. Add a Cloudflare Tunnel route (e.g. `grocy-mcp.yourdomain.com` -> `http://homeassistant:9193`)
3. In Claude.ai: **Settings > Integrations > Add MCP Server** > paste the full URL

## Links

- [grocy-mcp on PyPI](https://pypi.org/project/grocy-mcp/)
- [grocy-mcp source](https://github.com/moustafattia/grocy-mcp)
