"""Last.fm API integration for musicli."""

from __future__ import annotations

import os
from typing import Any

import pylast


_network: pylast.LastFMNetwork | None = None


def get_network() -> pylast.LastFMNetwork:
    """Return a lazy-initialised Last.fm network connection.

    Reads ``LASTFM_API_KEY`` and ``LASTFM_API_SECRET`` from the environment
    (or a ``.env`` file via python-dotenv if present).

    Raises:
        SystemExit: With a helpful message if credentials are missing.
    """
    global _network
    if _network is not None:
        return _network

    # Load .env if available
    try:
        from dotenv import load_dotenv

        load_dotenv()
    except ImportError:
        pass

    api_key = os.environ.get("LASTFM_API_KEY")
    api_secret = os.environ.get("LASTFM_API_SECRET")

    if not api_key or not api_secret:
        from rich.panel import Panel

        from musicli.ui.display import console

        console.print(
            Panel(
                "[bold red]❌ Last.fm credentials not found![/bold red]\n\n"
                "Please set the following environment variables:\n"
                "  [cyan]LASTFM_API_KEY[/cyan]=<your_key>\n"
                "  [cyan]LASTFM_API_SECRET[/cyan]=<your_secret>\n\n"
                "Or create a [bold].env[/bold] file in the current directory.\n"
                "Get a free key at [link=https://www.last.fm/api/account/create]"
                "https://www.last.fm/api/account/create[/link]",
                border_style="red",
                title="[bold red]Missing API Credentials[/bold red]",
            )
        )
        raise SystemExit(1)

    _network = pylast.LastFMNetwork(api_key=api_key, api_secret=api_secret)
    return _network


def reset_network() -> None:
    """Reset the cached network (used in tests)."""
    global _network
    _network = None


def get_artist_albums(artist_name: str) -> list[str]:
    """Return a sorted list of ``"Artist - Album"`` strings for *artist_name*.

    Filters out entries containing ``"(null)"``.

    Args:
        artist_name: The artist to look up on Last.fm.

    Returns:
        A sorted list of album strings prefixed with the artist name.

    Raises:
        pylast.PyLastError: If the artist is not found on Last.fm.
    """
    network = get_network()
    artist = network.get_artist(artist_name)
    top_albums = artist.get_top_albums()
    albums = [str(album.item) for album in top_albums]
    albums = [a for a in albums if "(null)" not in a]
    albums.sort()
    return albums


def get_album_tracks(artist: str, album: str) -> list[str]:
    """Return a list of track titles for the given artist/album.

    Args:
        artist: The artist name.
        album: The album title.

    Returns:
        A list of track title strings.
    """
    network = get_network()
    album_obj = network.get_album(artist, album)
    tracks = album_obj.get_tracks()
    return [t.title for t in tracks]


def get_album_cover_url(artist: str, album: str) -> str:
    """Return the cover art URL for the given artist/album.

    Falls back to a placeholder image URL on any error.

    Args:
        artist: The artist name.
        album: The album title.

    Returns:
        A URL string pointing to the album cover image.
    """
    _placeholder = (
        "https://community.mp3tag.de/uploads/default/original/2X/"
        "a/acf3edeb055e7b77114f9e393d1edeeda37e50c9.png"
    )
    try:
        import httpx

        network = get_network()
        album_obj = network.get_album(artist, album)
        cover_url = album_obj.get_cover_image()
        # Verify the URL is reachable
        response = httpx.get(cover_url, timeout=5)
        if response.status_code != 200:
            return _placeholder
        return cover_url
    except Exception:
        return _placeholder


def search_track(artist: str, song: str) -> Any | None:
    """Search Last.fm for a track.

    Args:
        artist: The artist name (used as a search hint).
        song: The song/track title.

    Returns:
        The first matching :class:`pylast.Track` object, or ``None``.
    """
    network = get_network()
    search = network.search_for_track(artist, song)
    results = search.get_next_page()
    return results[0] if results else None
