import time
from typing import Any, Dict, Optional

import httpx
import jwt


class AppleMusicClient:
    """
    Minimal Apple Music API client for catalog search and lookups.

    Uses a developer token (JWT) generated from your Apple Developer key.
    See: https://developer.apple.com/documentation/applemusicapi
    """

    def __init__(
        self,
        developer_token: str,
        storefront: str = "us",
        base_url: str = "https://api.music.apple.com/v1",
        http_timeout_seconds: float = 15.0,
    ) -> None:
        self.developer_token = developer_token
        self.storefront = storefront
        self.base_url = base_url.rstrip("/")
        self._client = httpx.Client(
            headers={"Authorization": f"Bearer {developer_token}"},
            timeout=http_timeout_seconds,
        )

    # ---- Catalog Search ----
    def search_catalog(
        self,
        term: str,
        types: str = "songs,albums,artists,playlists",
        limit: int = 10,
        offset: int = 0,
    ) -> Dict[str, Any]:
        params = {
            "term": term,
            "types": types,
            "limit": str(limit),
            "offset": str(offset),
        }
        url = f"{self.base_url}/catalog/{self.storefront}/search"
        response = self._client.get(url, params=params)
        response.raise_for_status()
        return response.json()

    # ---- Get by ID ----
    def get_song(self, song_id: str) -> Dict[str, Any]:
        url = f"{self.base_url}/catalog/{self.storefront}/songs/{song_id}"
        response = self._client.get(url)
        response.raise_for_status()
        return response.json()

    def get_album(self, album_id: str) -> Dict[str, Any]:
        url = f"{self.base_url}/catalog/{self.storefront}/albums/{album_id}"
        response = self._client.get(url)
        response.raise_for_status()
        return response.json()

    def get_artist(self, artist_id: str) -> Dict[str, Any]:
        url = f"{self.base_url}/catalog/{self.storefront}/artists/{artist_id}"
        response = self._client.get(url)
        response.raise_for_status()
        return response.json()

    def get_playlist(self, playlist_id: str) -> Dict[str, Any]:
        url = f"{self.base_url}/catalog/{self.storefront}/playlists/{playlist_id}"
        response = self._client.get(url)
        response.raise_for_status()
        return response.json()


def generate_developer_token(
    team_id: str,
    key_id: str,
    private_key_pem: str,
    expiry_seconds: int = 3600 * 12,
) -> str:
    """
    Generate a signed Apple Music API developer JWT.

    Provide the raw PEM private key string for your MusicKit key (starts with
    -----BEGIN PRIVATE KEY-----). The token should be used as the Bearer token
    for Apple Music API requests.
    """
    now = int(time.time())
    payload = {
        "iss": team_id,
        "iat": now,
        "exp": now + expiry_seconds,
    }
    headers = {"alg": "ES256", "kid": key_id}
    token = jwt.encode(payload, private_key_pem, algorithm="ES256", headers=headers)
    # pyjwt returns str for new versions
    return token  # type: ignore[return-value]
