"""Startup script for the Grocy MCP Home Assistant add-on."""

from __future__ import annotations

import json
import logging
import os
import re
import secrets
import sys
from pathlib import Path

import httpx

OPTIONS_PATH = Path("/data/options.json")
SECRET_PATH_FILE = Path("/data/secret_path.txt")
SECRET_PATH_RE = re.compile(r"^/(?!.*://)\S{7,}$")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    stream=sys.stdout,
)
log = logging.getLogger("grocy-mcp-addon")


def read_options() -> dict:
    """Read add-on options from HA Supervisor."""
    if OPTIONS_PATH.exists():
        return json.loads(OPTIONS_PATH.read_text())
    return {}


def generate_secret_path() -> str:
    """Generate a random secret path with 128-bit entropy."""
    return "/private_" + secrets.token_urlsafe(16)


def resolve_secret_path(configured: str) -> str:
    """Resolve the secret path: use configured, load persisted, or generate new."""
    # Use explicitly configured path
    if configured:
        if not SECRET_PATH_RE.match(configured):
            log.error(
                "Invalid secret_path '%s'. Must start with / and be at least 8 characters.",
                configured,
            )
            sys.exit(1)
        SECRET_PATH_FILE.write_text(configured)
        return configured

    # Load persisted path
    if SECRET_PATH_FILE.exists():
        persisted = SECRET_PATH_FILE.read_text().strip()
        if persisted and SECRET_PATH_RE.match(persisted):
            return persisted

    # Generate new path
    new_path = generate_secret_path()
    SECRET_PATH_FILE.write_text(new_path)
    return new_path


def check_grocy_connectivity(url: str, api_key: str) -> None:
    """Check if Grocy is reachable. Logs warning on failure, does not block startup."""
    try:
        resp = httpx.get(
            f"{url.rstrip('/')}/api/system/info",
            headers={"GROCY-API-KEY": api_key},
            timeout=5.0,
        )
        resp.raise_for_status()
        log.info("Grocy is reachable at %s", url)
    except Exception as exc:
        log.warning(
            "Grocy not reachable at %s — tools will fail until Grocy is available. Error: %s",
            url,
            exc,
        )


def main() -> None:
    """Main entry point."""
    options = read_options()

    grocy_url = options.get("grocy_url", "http://homeassistant.local:9192")
    grocy_api_key = options.get("grocy_api_key", "")
    port = options.get("port", 9193)
    secret_path = resolve_secret_path(options.get("secret_path", ""))

    if not grocy_api_key:
        log.error("grocy_api_key is required. Configure it in the add-on options.")
        sys.exit(1)

    # Set env vars for grocy-mcp's load_config()
    os.environ["GROCY_URL"] = grocy_url
    os.environ["GROCY_API_KEY"] = grocy_api_key

    # Startup connectivity check
    check_grocy_connectivity(grocy_url, grocy_api_key)

    # Log the MCP URL
    log.info("-----------------------------------------------------------")
    log.info("Grocy MCP Server is running!")
    log.info("MCP endpoint: http://homeassistant.local:%s%s", port, secret_path)
    log.info("-----------------------------------------------------------")

    # Import and start the server
    from grocy_mcp.mcp.server import create_mcp_server

    server = create_mcp_server()
    server.run(
        transport="streamable-http",
        host="0.0.0.0",
        port=port,
        path=secret_path,
        stateless_http=True,
    )


if __name__ == "__main__":
    main()
