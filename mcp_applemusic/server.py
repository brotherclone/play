import os
from typing import Any, Dict

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from mcp.server.stdio import stdio_server

from .client import AppleMusicClient


load_dotenv()


server = FastMCP("applemusic")


def _get_client() -> AppleMusicClient:
    developer_token = os.getenv("APPLE_MUSIC_DEVELOPER_TOKEN")
    storefront = os.getenv("APPLE_MUSIC_STOREFRONT", "us")
    if not developer_token:
        raise RuntimeError("APPLE_MUSIC_DEVELOPER_TOKEN env var is required")
    return AppleMusicClient(developer_token=developer_token, storefront=storefront)


@server.tool()
def search_catalog(term: str, types: str = "songs,albums,artists,playlists", limit: int = 10, offset: int = 0) -> Dict[str, Any]:
    """Search Apple Music catalog by term.

    Args:
        term: Search keywords.
        types: Comma-separated resource types to include.
        limit: Max number of results per type.
        offset: Pagination offset.
    """
    client = _get_client()
    return client.search_catalog(term=term, types=types, limit=limit, offset=offset)


@server.tool()
def get_song(song_id: str) -> Dict[str, Any]:
    """Get a catalog song by id."""
    client = _get_client()
    return client.get_song(song_id)


@server.tool()
def get_album(album_id: str) -> Dict[str, Any]:
    """Get a catalog album by id."""
    client = _get_client()
    return client.get_album(album_id)


@server.tool()
def get_artist(artist_id: str) -> Dict[str, Any]:
    """Get a catalog artist by id."""
    client = _get_client()
    return client.get_artist(artist_id)


@server.tool()
def get_playlist(playlist_id: str) -> Dict[str, Any]:
    """Get a catalog playlist by id."""
    client = _get_client()
    return client.get_playlist(playlist_id)


async def main() -> None:
    await server.run_stdio_async()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
