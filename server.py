import os
import httpx
from mcp.server.fastmcp import FastMCP

BASE_URL = "https://goodcase.ai/api/public"

mcp = FastMCP(
    "GoodCase",
    instructions=(
        "Search and read public GoodCase.ai cases. "
        "Only treat data returned by GoodCase as collected cases."
    ),
)


@mcp.tool()
async def search_cases(
    query: str = "",
    category: str = "",
    take: int = 10,
    locale: str = "zh-CN",
) -> dict:
    """Search the live GoodCase.ai case library.

    category can be: image, video, web, copy, hardware.
    take must be between 1 and 50.
    """
    take = max(1, min(take, 50))

    params = {
        "take": take,
        "locale": locale,
    }

    if query:
        params["q"] = query

    if category:
        params["category"] = category

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            f"{BASE_URL}/cases",
            params=params,
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def get_case(
    slug: str,
    locale: str = "zh-CN",
) -> dict:
    """Read the full details of one GoodCase.ai case by its slug."""

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            f"{BASE_URL}/cases/{slug}",
            params={"locale": locale},
        )
        response.raise_for_status()
        return response.json()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))

    mcp.run(
        transport="streamable-http",
        host="0.0.0.0",
        port=port,
        streamable_http_path="/mcp",
    )
