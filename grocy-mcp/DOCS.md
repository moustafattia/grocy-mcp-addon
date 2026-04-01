# Grocy MCP Server

This add-on runs [grocy-mcp](https://pypi.org/project/grocy-mcp/) as an HTTP MCP server, providing 80+ Grocy tools to AI agents like Claude and other MCP clients.

The current add-on release packages `grocy-mcp` `0.2.0`, including workflow helpers, planning surfaces, batteries, equipment, files, print actions, discovery helpers, and broader catalog access.

## Configuration

### Grocy URL

The URL of your Grocy instance. If Grocy runs as a Home Assistant add-on, use `http://homeassistant.local:9192`.

### Grocy API Key

Generate an API key in Grocy: **Settings > Manage API keys > Add**.

### Port

The HTTP port the MCP server listens on. Default: `9193`. Change only if it conflicts with another service.

### Secret Path

The MCP endpoint includes a secret URL path for security. By default, a random path is auto-generated on first start and persisted across restarts. You can set a custom path (must start with `/` and be at least 8 characters).

## Finding the MCP URL

After starting the add-on, check the **Log** tab. The startup banner shows the full MCP endpoint URL:

```
Grocy MCP Server is running!
MCP endpoint: http://<hostname>:9193/private_abc123...
```

## Remote Access via Cloudflare Tunnel

To use this add-on with Claude.ai, expose it via a Cloudflare Tunnel:

1. In the Cloudflared add-on, add a route: `grocy-mcp.yourdomain.com` -> `http://homeassistant:9193`
2. In Claude.ai: **Settings > Integrations > Add MCP Server**
3. Enter: `https://grocy-mcp.yourdomain.com/private_abc123...`
