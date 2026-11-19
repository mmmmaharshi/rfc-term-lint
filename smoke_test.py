"""Stdio smoke test: launch the server, list tools, call one. Run: uv run smoke_test.py"""

import anyio
import sys
from pathlib import Path

from mcp.client.session import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client


async def main():
    params = StdioServerParameters(
        command=sys.executable, args=[str(Path(__file__).with_name("server.py"))]
    )
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await session.list_tools()
            names = sorted(t.name for t in tools.tools)
            assert names == ["evaluate_text", "search_rfc_term", "suggest_fix"], names
            result = await session.call_tool("search_rfc_term", {"term": "MUST"})
            assert result.content, "empty tool result"
            print("smoke ok:", names)


anyio.run(main)
