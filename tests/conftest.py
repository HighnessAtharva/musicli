"""Shared pytest fixtures for the musicli test suite."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

import pytest


# ---------------------------------------------------------------------------
# Database fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def empty_db() -> dict[str, Any]:
    """Return an empty database dictionary."""
    return {"album_ratings": [], "song_ratings": [], "tier_lists": []}


@pytest.fixture
def sample_db() -> dict[str, Any]:
    """Return a database dictionary with realistic sample data."""
    return {
        "album_ratings": [
            {
                "artist": "Radiohead",
                "album": "OK Computer",
                "cover": "https://example.com/ok_computer.jpg",
                "album_rating": 10,
                "review": "A masterpiece of modern rock.",
                "time": "2024-01-15 12:00:00",
                "track_ratings": [
                    {"track": "Paranoid Android", "track_rating": 10},
                    {"track": "Karma Police", "track_rating": 9},
                ],
            },
            {
                "artist": "Radiohead",
                "album": "Kid A",
                "cover": "https://example.com/kid_a.jpg",
                "album_rating": 9,
                "review": "Bold and experimental.",
                "time": "2024-01-16 14:00:00",
                "track_ratings": [],
            },
            {
                "artist": "Nirvana",
                "album": "Nevermind",
                "cover": "https://example.com/nevermind.jpg",
                "album_rating": 8,
                "review": "",
                "time": "2024-02-01 09:30:00",
                "track_ratings": [],
            },
        ],
        "song_ratings": [
            {"track": "Smells Like Teen Spirit", "artist": "Nirvana", "track_rating": 9},
            {"track": "Creep", "artist": "Radiohead", "track_rating": 7},
        ],
        "tier_lists": [
            {
                "tier_list_name": "Radiohead Ranked",
                "artist": "Radiohead",
                "time": "2024-03-01 10:00:00",
                "s_tier": [{"album": "OK Computer", "cover_art": "https://example.com/ok.jpg"}],
                "a_tier": [{"album": "Kid A", "cover_art": "https://example.com/kida.jpg"}],
                "b_tier": [],
                "c_tier": [],
                "d_tier": [],
                "e_tier": [],
            }
        ],
    }


@pytest.fixture
def tmp_db(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Redirect all database I/O to a temp directory.

    Returns the path to the temporary database file.
    """
    from musicli.storage import db as db_module

    monkeypatch.setattr(db_module, "get_data_dir", lambda: tmp_path)
    monkeypatch.setattr(db_module, "get_db_path", lambda: tmp_path / "albums.json")
    monkeypatch.setattr(
        db_module,
        "get_output_dir",
        lambda: _make_output_dir(tmp_path),
    )
    return tmp_path / "albums.json"


def _make_output_dir(tmp_path: Path) -> Path:
    out = tmp_path / "output"
    out.mkdir(exist_ok=True)
    return out


@pytest.fixture
def tmp_db_with_data(tmp_db: Path, sample_db: dict[str, Any]) -> Path:
    """Populate the temp database with sample data."""
    import json

    tmp_db.write_text(json.dumps(sample_db), encoding="utf-8")
    return tmp_db


# ---------------------------------------------------------------------------
# Last.fm network mock
# ---------------------------------------------------------------------------


class _FakeTrack:
    """Minimal fake Track for tests."""

    def __init__(self, title: str = "Test Track", artist_name: str = "Test Artist") -> None:
        self.title = title
        self.artist = MagicMock()
        self.artist.name = artist_name


class _FakeAlbum:
    """Minimal fake Album for tests."""

    def __init__(self, name: str = "Test Artist - Test Album") -> None:
        self.item = name

    def __str__(self) -> str:
        return str(self.item)


class _FakeArtist:
    """Minimal fake Artist for tests."""

    def get_top_albums(self) -> list[_FakeAlbum]:
        return [
            _FakeAlbum("Radiohead - OK Computer"),
            _FakeAlbum("Radiohead - Kid A"),
            _FakeAlbum("Radiohead - (null)"),  # Should be filtered out
        ]


class _FakeNetwork:
    """Minimal fake LastFMNetwork for tests."""

    def get_artist(self, name: str) -> _FakeArtist:
        return _FakeArtist()

    def get_album(self, artist: str, album: str) -> MagicMock:
        m = MagicMock()
        m.get_cover_image.return_value = "https://example.com/cover.jpg"
        m.get_tracks.return_value = [_FakeTrack("Track 1"), _FakeTrack("Track 2")]
        return m

    def search_for_track(self, artist: str, song: str) -> MagicMock:
        m = MagicMock()
        m.get_next_page.return_value = [_FakeTrack(song, artist)]
        return m


@pytest.fixture
def mock_lastfm(monkeypatch: pytest.MonkeyPatch) -> _FakeNetwork:
    """Replace the live Last.fm network with a deterministic fake."""
    from musicli.core import lastfm as lastfm_module

    fake = _FakeNetwork()
    monkeypatch.setattr(lastfm_module, "_network", fake)
    return fake


# ---------------------------------------------------------------------------
# OpenAI mock
# ---------------------------------------------------------------------------


@pytest.fixture
def mock_openai(monkeypatch: pytest.MonkeyPatch) -> MagicMock:
    """Replace openai client with a mock that returns canned responses."""
    mock_client = MagicMock()
    mock_choice = MagicMock()
    mock_choice.message.content = "This is a test AI response."
    mock_client.chat.completions.create.return_value = MagicMock(choices=[mock_choice])

    with patch("musicli.ai.assistant._get_client", return_value=mock_client):
        yield mock_client


# ---------------------------------------------------------------------------
# HTTP mock (for cover art / image downloads)
# ---------------------------------------------------------------------------


@pytest.fixture
def mock_http(monkeypatch: pytest.MonkeyPatch) -> None:
    """Mock httpx.get to return a tiny 1x1 red PNG."""
    import io

    from PIL import Image

    # Create a 1x1 red JPEG-style PNG in memory
    img = Image.new("RGB", (1, 1), color=(200, 50, 50))
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    png_bytes = buf.getvalue()

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.content = png_bytes

    monkeypatch.setattr("httpx.get", lambda *args, **kwargs: mock_response)
